"""
----------------------------------------------------------------------------
| This file will contain all the forms that we will use on the application |
----------------------------------------------------------------------------
"""
# Flask forms will be used to make forms for submissions
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from quizaris.database import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign up')

	# The following set of validation functions will check whether the user data exists in order to avoid conflicts in the database
	def validate_username(self, username):
		# If the username exists this user = True if not it will be None 
		user  = User.query.filter_by(username=username.data).first()
		if user:
			# Validation error is built in to the wtforms.validators library
			raise ValidationError('The username already exists! Please pick a different username!')

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError('A user with that email already exists')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')