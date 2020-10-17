"""
----------------------------------------
| This file will contain all the routes|
----------------------------------------
"""

# Import the app 
from quizaris import app, db, bcrypt
# Import the database models/tables from the database.py file. 
from quizaris.database import User, Question
# Only import the relevant stuff for this file.
from flask import render_template, url_for, flash, redirect
# import the forms 	
from quizaris.forms import *
# Import the login function from the database file
from flask_login import login_user, current_user, logout_user, login_required


# The following routes are used to route the users to the intended locations
@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return url_for('home')

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        # The user variable will store the data returned by the query that if a user exists will return a value,
        # else it will return none
        user = User.query.filter_by(email=email).first()
        # Check if the users data matches with the data returned in the above query
        if user and bcrypt.check_password_hash(user.password, password):
            # The following function call will log the user in and create a session for them.
            login_user(user, False)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful please check your email or password')
    # The form variable is passed in to the form for jinja being able to access it.
    # The variables passed in are form, and title which will be used with jinja
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return url_for('home')
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        # Generate a password hash from the user entered password. decode will convert the bytes to a string.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Creat the user instance
        user = User(username=username, email=email, password=hashed_password)
        # Add the data to the database
        db.session.add(user)
        db.session.commit()

        flash('Created account', 'success')
        # Redirect to the url of the home() function
        return redirect("/login")
    return render_template('register.html', title="Register", form=form)


@app.route("/addquiz", methods=['GET', 'POST'])
@login_required
def addquiz():
    # Forms is an array that will contain all the Add question form instances.
    # Use the index while accessing these with jinja
    add_question_forms = []
    for i in range(10):
        add_question_forms.append(AddQuestion(prefix="form"+str(i)))
    # MakeQuiz instance
    quiz_form = MakeQuiz()
    current_users_data = User.query.filter_by(email=current_user.email).first()
    # Check if the questions submitted are more than 5
    print("UQUIZ")
    if quiz_form.quizname.data:
        print("Quiz is being submitted")
        add_quiz = Quiz(quizname=quiz_form.quizname.data, category=quiz_form.category.data,
                        difficulty=quiz_form.difficulty.data, user_id=current_users_data.id)
        db.session.add(add_quiz)
        db.session.commit()
        # After comitting the quiz we need to retrieve its id to use for adding forms
        get_quiz_id = Quiz.query.filter_by(quizname=quiz_form.quizname.data, category=quiz_form.category.data,
                        difficulty=quiz_form.difficulty.data, user_id=current_users_data.id).first()
        print("submit")
        for i in range(10):

            if add_question_forms[i].validate():
                print(add_question_forms[i])
                add_question = Question(question=add_question_forms[i].question.data,
                                        option_a=add_question_forms[i].option_a.data,
                                        option_b=add_question_forms[i].option_b.data,
                                        option_c=add_question_forms[i].option_c.data,
                                        option_d=add_question_forms[i].option_d.data, answer=add_question_forms[i].answer.data, solution_explanation=add_question_forms[i].solution_explanation.data ,user_id=current_users_data.id, quiz_id=get_quiz_id.id )
                db.session.add(add_question)
                db.session.commit()

    # The forms variable is an array that contains 10 instances of the AddQuestion form.
    return render_template("addquiz.html", title="Add Questions", add_question_forms=add_question_forms, quiz_form=quiz_form)


# The following function will route to quizzes and allow the user to view the quizzes.
@app.route("/quizzes", methods=['GET', 'POST'])
@login_required
def quizzes():
    # A search form which will be used to look for forms.
    search_form = Search()
    choose_quiz_type_form = ChooseTypeQuiz()
    select_quiz_to_do = SelectWhatQuiz()
    if choose_quiz_type_form.validate_on_submit():
        if choose_quiz_type_form.category:
            # This will be an array of questions so use a for loop in jinja
            possible_quizzes = Quiz.query.filter_by(category=choose_quiz_type_form.category).all()
        elif choose_quiz_type_form.difficulty:
            # This will be an array of questions so use a for loop in jinja
            possible_quizzes = Quiz.query.filter_by(category=choose_quiz_type_form.category, difficulty=choose_quiz_type_form.difficulty).all()
        elif choose_quiz_type_form.difficulty and choose_quiz_type_form.category:
            # This will be an array of questions so use a for loop in jinja
            possible_quizzes = Quiz.query.filter_by(category=choose_quiz_type_form.category, difficulty=choose_quiz_type_form.difficulty).all()
    else:
        # This will be an array of questions so use a for loop in jinja
        # If no filters have been applied all the Quizzes are returned
        possible_quizzes = Quiz.query.all()
    if select_quiz_to_do.validate_on_submit():
        # Call the function quiz which would do the quiz for us.
        # The following url for will grab the data from the quiz_id/ creates a dynamic route to it and allows the user to do the quiz.
        return redirect(url_for('quiz', quiz_id=select_quiz_to_do.select_box_quizzes.data))
    # The variables form, title and search_form are passed in to the template. The forms fields can be found in the
    # forms.py file.
    # List all the possible quizzes using a radio
    # Possible quizzes is the data RETURNED by the database. So we are looking at using possible_quizzes[i].{valuies that are in the db }
    return render_template('quizzes.html', title='Quizzes', choose_quiz_type_form=choose_quiz_type_form, possible_quizzes=possible_quizzes, search_form=search_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# The following function will be used to do the quiz themself.
@app.route("/quiz/<quiz_id>")
@login_required
def quiz(quiz_id):
    # This will return an array of questions that have the quiz_id of the current quiz
    current_quiz_questions = Question.query.filter_by(id=quiz_id).all()
    # These are the variables set which should be displayed at the end.
    correct_answers = 0
    wrong_answers = 0
    # This will be an array of questions so use a for loop in jinja
    submit_quiz = SubmitQuiz()
    solve_question_array = []
    for i in current_quiz_questions:
        solve_question_array.append(i)
    if submit_quiz.validate_on_submit():
        for i in range(10):
            # The following try will avoid any index out of bounds errors
            try:
                if solve_question_array[i].validate():
                    if solve_question_array[i].options.data == current_quiz_questions[i].answer:
                        correct_answers += 1
                    else:
                        wrong_answers += 1
            except:
                pass

    # Solve questions array is a an array that will contain all the form objects, so, like before use index's to get the form labels and input fields.
    return render_template('quiz.html', current_quiz_questions=solve_question_array, correct_answers=correct_answers, wrong_answers=wrong_answers)

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    current_users_data = User.query.filter_by(email=current_user.email).first()
    quizzes_done = CompletedQuizzes.query.filter_by(user_id=current_users_data.id)
    return render_template('account.html', username=current_user.username, email=current_user.email, quizzes_done=quizzes_done)
