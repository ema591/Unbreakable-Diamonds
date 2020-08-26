from flask import Flask, render_template, url_for
# Import form from the forms.py file
from forms import RegistrationForm, LoginForm
# Creating an instance of flask
app = Flask(__name__)

# Set a cookie to avoid CSRF attacks
app.config['SECRET_KEY'] = '23ac083317c8fd13abc6e424e9425b4f'

posts = [
	{
		'author': 'Me',
		'title': 'KAKAKAK',
		'content': 'First question',
		'date_posted': 'Today'
	}, 
	{
		'author': 'You',
		'title': 'NayNay',
		'content': 'Second Questions',
		'date_posted': 'last nmight'
	}
]

# The following routes are used to route the users to the intended locations
@app.route("/")
def hello():
	return "<h1>Index page<h1>"

@app.route("/test")
def team():
	return render_template("test.html", posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	return render_template('test-form.html', title="Test", form=form)

# @app.route("/login")
# def register():
# 	form = LoginForm()
# 	return render_template('test-form.html', title="Test", form=form)