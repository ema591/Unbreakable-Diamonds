from flask import Flask, render_template
# Creating an instance of flask
app = Flask(__name__)

posts = [
	{
		'author': 'Test',
		'title': 'testing',
		'content': 'First question',
		'date_posted': 'Today'
	}
]

# The following routes are used to route the users to the intended locations
@app.route("/")
def hello():
	return "<h1>Index page<h1>"

@app.route("/test")
def team():
	return render_template("test.html", posts=posts)

