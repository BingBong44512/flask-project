from flask import Flask, request, jsonify, render_template, redirect,url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_login import login_user, logout_user, current_user, UserMixin, login_required
from app import app, login_manager, db, admin
from .forms import LoginForm, RegisterForm, ChangePassword
from .models import User
from .common import cache
import json
# sets up the login manager to work with the app
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."
# loads in the user
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
# home page
@app.route('/')
def index():
	return render_template('index.html')
# uses teh login in form to check if some has logged in
@app.route('/login', methods=["POST","GET"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		remember = form.remember_me.data

		user = User.query.filter_by(username=username).first()
		if user and username == user.username and user.check_password(password):
			login_user(user, remember=remember)
			flash('Logged in successfully.')
			next = request.args.get('next')
		else:
			
			flash('Invalid username or password (temporary)')
			return render_template('login.html', form=form)
			
		#if not url_has_allowed_host_and_scheme(next, request.host):
		#	return flask.abort(400)
		return redirect(next or url_for('profile'))
	return render_template('login.html', form=form)
# uses the register form to see if they can be registered, and to do so
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RegisterForm()
	if form.validate_on_submit():
		username = form.username.data.strip()
		email = form.email.data.strip().lower()
		password = form.password.data

		existing_user = User.query.filter(
			(User.username == username)).first()

		if existing_user:
			flash("Username or email already registered.")
			return render_template('register.html', form=form)

		new_user = User(username=username, email=email, password=password)
		db.session.add(new_user)
		db.session.commit()

		login_user(new_user)
		flash('Registration successful!')
		return redirect(url_for('profile'))

	return render_template('register.html', form=form)
# calls the change password function on the database model, using the form to check it
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_pass():
	form = ChangePassword()
	if request.method == "POST" and form.validate_on_submit():
		if current_user.check_password(form.current_password.data):
			current_user.set_password(form.new_password.data)
			db.session.commit()
			return redirect(url_for('profile'))

	return render_template('change_pass.html', form=form)
# logsout the user via the flask login
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

# opens te profile page if needed
@app.route("/profile")
@login_required
def profile():
	if current_user.is_authenticated:
		return render_template("profile.html")
	else:
		return redirect(url_for("index"))
# takes necessary information from cache and puts it into the render template for jinja
@app.route('/text')
def text():

	# if form.validate_on_submit():
	# 	return redirect(url_for('index'))

	return render_template('texty.html',inputText = cache.get("inputText"),correctAnswers = cache.get("correctAnswers"),lessonName = cache.get("lessonName")
		,link = cache.get("link"))
