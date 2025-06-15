import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'DO_NOT_USE_IN_PROD'

	# Flask application settings
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'DO_NOT_USE_IN_PROD!!!!'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Flask-Mail settings
	MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None or True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'ycc2238@gmail.com'
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-email-password'
	MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'ycc2238@gmail.com'
	SERVER_NAME = os.environ.get('SERVER_NAME') or 'localhost:8080'