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
from quizaris.forms import RegistrationForm, LoginForm

# The following routes are used to route the users to the intended locations
@app.route("/")
def home():
	
	return '<h1>Hello</h1>'
@app.route("/test")
def test():
	return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		# username = form.username.data

		flash('Login successful')
	return render_template("login.html", title="Login",  form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
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
