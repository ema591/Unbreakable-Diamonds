"""
----------------------------------------------------------------------------
| This file will contain all the forms that we will use on the application |
----------------------------------------------------------------------------
"""
# Flask forms will be used to make forms for submissions
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from quizaris.database import *


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign up')

    # The following set of validation functions will check whether the user data exists in order to avoid conflicts
    # in the database
    def validate_username(self, username):
        # If the username exists this user = True if not it will be None
        user = User.query.filter_by(username=username.data).first()
        if user:
            # Validation error is built in to the wtforms.validators library and will be returned as a form error.
            raise ValidationError('The username already exists! Please pick a different username!')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('A user with that email already exists')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddQuestion(FlaskForm):
    question = StringField('Question', validators=[DataRequired()], render_kw={"placeholder": "Question"})
    option_a = StringField('Option A', validators=[DataRequired()], render_kw={"placeholder": "Option A"})
    option_b = StringField('Option B', validators=[DataRequired()], render_kw={"placeholder": "Option B"})
    option_c = StringField('Option C', render_kw={"placeholder": "Option C"})
    option_d = StringField('Option D', render_kw={"placeholder": "Option D"})
    answer = IntegerField('Answer', validators=[DataRequired()],
                          render_kw={"placeholder": "1 for A, 2 for B, 3 for C, 4 for D"})
    solution_explanation = StringField('Explanation', validators=[DataRequired()], render_kw={"placeholder": "Explanantion for the solution"})
    submit = SubmitField('Submit Question')


# The following form will be used by the users to choose the type of quiz that they want to do.
class ChooseTypeQuiz(FlaskForm):
    category = SelectField('Category', choices=[('science', 'Science'), ('maths', 'Maths'), ('english', 'English'), ('business', 'Business')])
    difficulty = SelectField('Difficulty',
                             choices=[('easy', 'Easy'), ('intermediate', 'Intermediate'), ('hard', 'Hard')])
    submit = SubmitField('Choose quiz')


# pass in keyword args (kwargs) with a key value pair like a dictionary
class SolveQuestion(FlaskForm):
    # options = RadioField('Options', choices=[('1', "lala")])
    def __init__(self, **kwargs):
        self.question_id = kwargs['question_id']
        self.question_name = kwargs['question_name']
        self.option_a = kwargs['option_a']
        self.option_b = kwargs['option_b']
        self.option_c = kwargs['option_c']
        self.option_d = kwargs['option_d']
        self.options = RadioField('Options',
                                 choices=[('1', self.option_a), ('2', self.option_b), ('3', self.option_c),
                                          ('4', self.option_d)])
        super().__init__()

class SubmitQuiz(FlaskForm):
    submit = SubmitField('Submit Quiz')

class Search(FlaskForm):
    search = StringField('Search', render_kw={"placeholder": "search field"})


class MakeQuiz(FlaskForm):
    quizname = StringField('Quizname', validators=[DataRequired()], render_kw={"placeholder": "Quiz name here"})
    category = SelectField('Category',
                           choices=[('science', 'Science'), ('it', 'Information Technology'), ('maths', 'Maths'),
                                    ('english', 'English'), ('business', 'Business')])
    difficulty = SelectField('Difficulty',
                             choices=[('easy', 'Easy'), ('intermediate', 'Intermediate'), ('hard', 'Hard')])
    submit = SubmitField('Make Quiz')


