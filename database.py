from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizaris.db'
db = SQLAlchemy(app)

# The table name will be `user` - lowercase
class User(db.Model):
	# Makes coloumns for the user data.
	_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
	username = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	password = db.Column(db.String(60), nullable=False)
	# adding a relationship between the User and any questions that they make.
	# This question exists here because of the cardinality of the relationship i.e. 1 user can make multiple questions but a question can only have 1 author
	question = db.relationship('Question', backref='author', lazy=True) # Lazy true means that sqlalchemy will load all the data in one go 
	# Way the data is displayed when looking at the object
	def __repr__(self):
		return f"User('{self._id}', '{self.username}', '{self.email}')"

# The table name will be `question` - lowercase
class Question(db.Model):
	_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
	question = db.Column(db.String(150), nullable=False)
	option_a = db.Column(db.String(150), nullable=False)
	option_b = db.Column(db.String(150), nullable=False)
	# The nullables for the following are true as they do not have to be there for e.g. when using True False questions
	option_c = db.Column(db.String(150), nullable=True)
	option_d = db.Column(db.String(150), nullable=True)
	# The answer will be stored as an integer 1-4 and each will correspond to an option.
	answer = db.Column(db.Integer, nullable=False)
	# Category of the questions will be stored here
	category = db.Column(db.String(30), nullable=False)
	# The following column will contain the foreign key containing the id of the user who created the question.
	user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
	# Way the data is displayed when looking at the object
	def __repr__(self):
		return f"Question('{self._id}, {self.question}, {self.answer}')"

# class Progress(db.Model):
# 	solver = db.relationship('User')
# 	questions_solved = db.relationship('Question', 'solved_by')

