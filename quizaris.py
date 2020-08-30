from flask import Flask, render_template, url_for, flash, redirect
# Import form from the forms.py file
from forms import RegistrationForm, LoginForm
# Creating an instance of flask
app = Flask(__name__)

# Set a cookie to avoid CSRF attacks
app.config['SECRET_KEY'] = '23ac083317c8fd13abc6e424e9425b4f'

# The following routes are used to route the users to the intended locations
@app.route("/")
def home():
	return "<h1>Index page<h1>"

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form['']
		flash('Login successful')
	return render_template("login.html", title="Login",  form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash('Created account')
		# Redirect to the url of the home() function
		return redirect("/")
	return render_template('register.html', title="Register", form=form)

# @app.route("/login")
# def register():
# 	form = LoginForm()
# 	return render_template('test-form.html', title="Test", form=form)