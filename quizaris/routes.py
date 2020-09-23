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
from quizaris.forms import RegistrationForm, LoginForm, ChooseTypeQuiz, AddQuestion
# Import the login function from the database file
from flask_login import login_user, current_user, logout_user, login_required


# The following routes are used to route the users to the intended locations
@app.route("/")
def home():
    return ''


@app.route("/test")
def test():
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
        user = User.query.filter_by(email=email)
        # Check if the users data matches with the data returned in the above query
        if user and bcrypt.check_password_hash(user.password, password):
            # The following function call will log the user in and create a session for them.
            login_user(user, remember_me)
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


@app.route("/questions")
@login_required
def questions():
    form = AddQuestion()
    if form.validate_on_submit():
        # collect all the data from the form.
        question = form.question.data
        answer = form.answer.data
        option_a = form.option_a.data
        option_b = form.option_b.data
        option_c = form.option_c.data
        option_d = form.option_d.data
        category = form.category.data
        difficulty = form.difficulty.data
        add_question = AddQuestion(question=question, answer=answer, option_d=option_d, option_c=option_c,
                                   option_b=option_b, option_a=option_a, difficulty=difficulty)
    return render_template("questions.html", title="Add Questions", form=form)


# The following function will route to quizzes and allow the user to interact with the quizzes.
@app.route("/quizzes")
@login_required
def quizzes():
    form = ChooseTypeQuiz()
    return render_template('quizzes.html', title='Quizzes', form=form)


@app.route("/logout")
def logout():
    logout_user()


@app.route("/account")
@login_required
def account():
    return ""
