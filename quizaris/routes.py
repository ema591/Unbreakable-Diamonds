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


@app.route("/questions", methods=['GET', 'POST'])
@login_required
def questions():
    # Forms is an array that will contain all the Add question form instances.
    # Use the index while accessing these with jinja
    add_question_forms = []
    for i in range(10):
        add_question_forms[i] = AddQuestion()
    # MakeQuiz instance
    quiz_form = MakeQuiz()
    # Keeps count of the valid questions.
    valid_questions = 0
    for i in range(10):
        if add_question_forms[i].validate_on_submit():
            add_question = Question(question=add_question_forms[i].question, option_a=add_question_forms[i].option_a,
                                    option_b=add_question_forms[i].option_b, option_c=add_question_forms[i].option_c,
                                    option_d=add_question_forms[i].option_d)
            db.session.add(add_question)
            db.session.commit()
            valid_questions += 1
    # Check if the questions submitted are more than 5
    if valid_questions > 5 and quiz_form.validate_on_submit():
        author = User.query.filter_by(email=current_user.email).first()
        add_quiz = Quiz(quizname=quiz_form.quizname.data, category=quiz_form.category.data,
                        difficulty=quiz_form.difficulty.data, user_id=author.id)
        db.session.add(add_quiz)
        db.session.commit()

    # The forms variable is an array that contains 10 instances of the AddQuestion form.
    return render_template("questions.html", title="Add Questions", forms=add_question_forms, quiz_form=quiz_form)


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
        return redirect(url_for('quiz', quiz_id=select_quiz_to_do.select_box_quizzes.data))
    # The variables form, title and search_form are passed in to the template. The forms fields can be found in the
    # forms.py file.
    # List all the possible quizzes using a radio
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
    # current_quiz = Quiz.query.filter_by(id=quiz_id).first()
    # This will be an array of questions so use a for loop in jinja
    # the_questions = Question.query.filter_by(quiz_id=quiz_id).all()
    # solve_quiz = SolveQuiz()
    # if solve_quiz.validate_on_submit():
    #     selected_answer =
    return render_template('quiz.html', the_questions=the_questions)

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    current_users_data = User.query.filter_by(email=current_user.email).first()
    quizzes_done = CompletedQuizzes.query.filter_by(user_id=current_users_data.id)
    return render_template('account.html', username=current_user.username, email=current_user.email, quizzes_done=quizzes_done)
