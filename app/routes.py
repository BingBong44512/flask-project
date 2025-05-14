from flask import Flask, request, jsonify, render_template, redirect,url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_user, logout_user, current_user, UserMixin, login_required
from app import app, login_manager, db
from app.forms import LoginForm

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

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

		user = User.query.filter_by(username=username).first()
		if username == temp_user.username and temp_user.check_password(password):
			login_user(temp_user, remember=remember)
			flash('Logged in successfully.')
			next = request.args.get('next')
		else:
			flash('Invalid username or password (temporary)')
			return render_template('login.html', form=form)
			
		if not url_has_allowed_host_and_scheme(next, request.host):
			return flask.abort(400)
		return redirect(next or url_for('user', username=username))
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		flash('User not found')
		return redirect(url_for('index'))
	return render_template('user.html', username=username)