from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
# creates different forms to be used
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
	email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
	confirm_password = PasswordField('Confirm Password', validators=[
		DataRequired(), EqualTo('password', message='Passwords must match.')
	])
	submit = SubmitField('Register')

class ChangePassword(FlaskForm):
	current_password = PasswordField('Password', validators=[DataRequired()])

	new_password = PasswordField('New Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[
		DataRequired(), EqualTo('new_password', message='Passwords must match.')
	])

	submit = SubmitField('Change Password')

class TextForm(FlaskForm):
	submit = SubmitField('Submit')

class AdminCodeForm(FlaskForm):
	admin_code = PasswordField('Admin Code', validators=[DataRequired()])
	submit     = SubmitField('Submit')
