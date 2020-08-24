from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/noob/Desktop/Flask_app/Unbreakable-Diamonds/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	# Define table name
	__tablename__ = "user"

	# Makes three columns
	_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False)

	def __init__(self, name, email):
		self.name = name
		self.email = email

new_data = User("admin", "admin@admin.com")
db.session.add(new_data)
db.session.commit()

user_data = User.query.all()
print()