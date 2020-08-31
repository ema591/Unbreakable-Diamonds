"""
----------------------------------------------------------------------------------------
| This file will contain all the initializing data like the app itself and the database|
---------------------------------------------------------------------------------------
"""
from flask import Flask
# Import form from the forms.py file
from flask_sqlalchemy import SQLAlchemy
# The following library will allow us to set a password hash.
from flask_bcrypt import Bcrypt
# Import the flask login manager which will be used to handle Logins
from flask_login import LoginManager

# Configurations 

# Creating an instance of flask
app = Flask(__name__)
# Set a Secret key to avoid CSRF attacks
app.config['SECRET_KEY'] = '23ac083317c8fd13abc6e424e9425b4f'
# Setup a database instance for the app.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizaris.db'
# Initialize a database instance.
db = SQLAlchemy(app)
# Initialize bcrypt.
bcrypt = Bcrypt(app)
# Create a LoginManager instance for the application.
# login_manager = LoginManager(app)

# Import the routes 
from quizaris import routes 