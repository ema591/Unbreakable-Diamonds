"""
-----------------------------------------------------------------------------------------
| This file will contain all the database tables/models which will be used to store data|
-----------------------------------------------------------------------------------------
"""

"""
TODO:
Add another class which will store the users quiz data. TBD what kind of data we are storing. 
"""

# Import the db instance and the login manager instance from the __init__.py file.
from quizaris import db, login_manager
# Import UserMixin for keeping track of authenticated users.
from flask_login import UserMixin


# For the login manager we need to be able to identify a user with their ID
@login_manager.user_loader
def load_user(user_id):
    # The function will simply return the user with the user_id set to the param.
    return User.query.get(int(user_id))


# The table name will be `user` - lowercase
class User(db.Model, UserMixin):
    # Makes columns for the user data.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # adding a relationship between the User and any questions that they make. This question exists here because of
    # the cardinality of the relationship i.e. 1 user can make multiple questions but a question can only have 1 author
    quiz = db.relationship('Quiz', backref='author',
                           lazy=True)  # Lazy true means that sqlalchemy will load all the data in one go

    # Way the data is displayed when looking at the object
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"


# The table name will be `question` - lowercase
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(150), nullable=False)
    option_a = db.Column(db.String(150), nullable=False)
    option_b = db.Column(db.String(150), nullable=False)
    # The nullables for the following are true as they do not have to be there for e.g. when using True False questions
    option_c = db.Column(db.String(150), nullable=True)
    option_d = db.Column(db.String(150), nullable=True)
    # The answer will be stored as an integer 1-4 and each will correspond to an option.
    answer = db.Column(db.Integer, nullable=False)
    solution_explanation = db.Column(db.String(250),
                                     default="The author has not added an explanation for the solution")
    # The following column will contain the foreign key containing the id of the user who created the question.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    # Way the data is displayed when looking at the object
    def __repr__(self):
        return f"Question('{self.id}, {self.question}, {self.answer}')"


class CompletedQuizzes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # One quiz can have multiple questions
    questions = db.relationship('Question', backref='quiz_questions', lazy=True)
    quizname = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comments', backref='comments',
                               lazy=True)  # Lazy true means that sqlalchemy will load all the data in one go
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    # Category of the questions will be stored here
    category = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Quiz('{self.quizname}')"


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # Comments themselves
    comment = db.Column(db.String(200))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # Rating will be calculated out of five and thus will be stored as an integer.
    user_rating = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
