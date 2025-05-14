from flask_login import UserMixin
from wekzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()

class User(UserMixin, Base):

	__tablename__ = 'users'

	id = Column(integer, primary_key=True)
	username = Column(String(80), unique=True, nullable=False)
	email = Column(String(120), unique=True, nullable=False)
	#later we will need to add email authentication!!!
	password_hash = Column(String(128), nullable=False)

	def __init__(self, username, email, password):

		self.username = username
		self.email = email
		self.set_password(password)

	def set_password(self, password):

		self.password_hash = generate_password_hash(password)

	def check_password(self, password):

		return check_password_hash(self.password_hash, password)

	def __repr__(self):

		return f'<User(username = {self.username}, email = {self.email})>'
