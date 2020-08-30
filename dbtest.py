from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizaris.db'
db = SQLAlchemy(app)

class User(db.Model):
	# Makes three columns
	_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
	username = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	password = db.Column(db.String(60), nullable=False)
	
	def __repr__():
		return f"User('{self._id}', '{self.name}', '{self.email}')"


def Question(db.Model):
	_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
	question = db.Column(db.String(150), nullable=False)
	option_a = db.Column(db.String(150), nullable=False)
	option_b = db.Column(db.String(150), nullable=False)
	# The nullables for the following are true as they do not have to be there for e.g. when using True False questions
	option_c = db.Column(db.String(150), nullable=True)
	option_d = db.Column(db.String(150), nullable=True)
	# The answer will be stored as an integer 1-4 and each will correspond to an option.
	answer = db.Column(db.Integer, nullable=False)

	def __repr__():
		return f"Question('{self._id}, {self.question}, {self.answer}')"


# new_data = User("admin", "admin@admin.com", "76tg8sdAS9Y8d")
# db.session.add(new_data)
# db.session.commit()

# user_data = User.query.all()
# print()