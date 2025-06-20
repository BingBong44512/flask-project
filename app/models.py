from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db

# creates the database model for the user, with various functions for it
class User(UserMixin, db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	points = db.Column(db.Integer, default=0)
	password_hash = db.Column(db.String(128), nullable=False)
	email_verified = db.Column(db.Boolean, default=False)
	email_verification_token = db.Column(db.String(128), unique=True, nullable=True)

	is_admin = db.Column(db.Boolean, default=False)

	def __init__(self, username, email, password):

		self.username = username
		self.email = email
		self.set_password(password)

	def set_password(self, password):

		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_name(self):
		return self.username

	def __repr__(self):

		return f'<User(username = {self.username}, email = {self.email})>'
