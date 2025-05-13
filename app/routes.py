from flask import Flask, request, jsonify, render_template, redirect,url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_user, logout_user, current_user, UserMixin, login_required
from app import app, login_manager
from app.forms import LoginForm

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."

class TempUser(UserMixin):
	def __init__(self, id, username, password):
		self.id = id
		self.username = username
		self.pass1 = password

	def check_password(self, password):
		if(self.pass1==password):
			return True
		else:
			return False

temp_user = TempUser(1, "test", "admin")

@login_manager.user_loader
def load_user(user_id):
	return 1

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=["POST","GET"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		remember = form.remember_me.data

		print("akhfh")
		if username == temp_user.username and temp_user.check_password(password):
			login_user(temp_user, remember=remember)
			flash('Logged in successfully.')
			next_page = request.args.get('next')
			if not next_page or not next_page.startswith('/'):
				next_page = url_for('index')
			return redirect(url_for('user', username=username))
		else:
			flash('Invalid username or password (temporary)')
			return render_template('login.html', form=form)
			
		if not url_has_allowed_host_and_scheme(next, request.host):
			return flask.abort(400)
		return redirect(next or flask.url_for('user.html'))
	return render_template('login.html', form=form)

@app.route('/user/<username>')
#@login_required
def user(username):
	return render_template('user.html', username=username)