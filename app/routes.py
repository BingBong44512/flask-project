from flask import Flask, request, jsonify, render_template, redirect,url_for, session, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_login import login_user, logout_user, current_user, UserMixin, login_required
from flask_mailman import EmailMessage
from app import app, login_manager, db, admin, mail
from .forms import LoginForm, RegisterForm, ChangePassword, TextForm, AdminCodeForm
from flask_principal import identity_changed, Identity
from .models import User
from .common import cache
import json
import secrets

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route('/')
def index():
	username = ""
	if current_user.is_authenticated:
		username = current_user.username
	return render_template('index.html', username = username)

@app.route('/login', methods=["POST","GET"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		remember = form.remember_me.data

		user = User.query.filter_by(username=username).first()
		if user and username == user.username and user.check_password(password):

			if not user.email_verified:
				flash('Please verify your email address before logging in.')
				return render_template('login.html', form=form)

			login_user(user, remember=remember)
			identity_changed.send(
			current_app._get_current_object(),
			identity=Identity(user.id)
			)

			flash('Logged in successfully.')
			next = request.args.get('next')
		else:
			flash('Invalid username or password (temporary)')
			return render_template('login.html', form=form)
			
		#if not url_has_allowed_host_and_scheme(next, request.host):
		#	return flask.abort(400)
		return redirect(next or url_for('profile'))
	return render_template('login.html', form=form)

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
			(User.username == username) | (User.email == email)
			).first()

		if existing_user:
			if existing_user.username == username:
				flash("Username already registered.")
			elif existing_user.email == email:
				flash("Email already registered.")
			return render_template('register.html', form=form)

		new_user = User(username=username, email=email, password=password)

		verification_token = secrets.token_urlsafe(32)
		new_user.email_verification_token = verification_token
		new_user.email_verified = False

		db.session.add(new_user)
		db.session.commit()

		msg = EmailMessage(
			subject='Verify Your Email Address for Thinkful',
			body=f"""
				Hello {new_user.username},

				Thank you for registering on our website!
				Please click on the following link to verify your email address:

				{url_for('verify_email', token=verification_token, _external=True)}

				If you did not register for this account, please ignore this email.

				Sincerely,
				The Website Team
				""",
					to=[new_user.email]
		)

		try:
			msg.send()
			flash('Registration successful! Please check your email to verify your account.')
			return redirect(url_for('login'))
		except Exception as e:
			db.session.rollback()
			print(f"Error sending email: {e}")
			flash(f'Registration failed: Could not send verification email. Please try again. Error: {e}')
			return render_template('register.html', form=form)

	return render_template('register.html', form=form)

@app.route('/verify_email/<token>')
def verify_email(token):
	user = User.query.filter_by(email_verification_token=token).first()

	if user:
		user.email_verified = True
		user.email_verification_token = None # Clear the token after verification
		db.session.commit()
		flash('Your email has been successfully verified! You are now logged in.')
		login_user(user)
		return redirect(url_for('profile'))
	else:
		flash('Invalid or expired verification link.')
		return redirect(url_for('index'))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_pass():
	form = ChangePassword()
	if form.validate_on_submit():
		current_user.set_password(form.new_password.data)
		db.session.commit()
		return redirect(url_for('profile'))

	return render_template('change_pass.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	identity_changed.send(
		current_app._get_current_object(),
		identity=AnonymousIdentity()
	)
	return redirect(url_for('index'))



@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		flash('User not found')
		return redirect(url_for('index'))
	return render_template('user.html', username=username)

@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html')

@app.route('/text', methods = ['GET', 'POST'])
def text():
	form = TextForm()

	if form.validate_on_submit():
		return redirect(url_for('index'))

	return render_template('texty.html',inputText = cache.get("inputText"),correctAnswers = cache.get("correctAnswers"),lessonName = cache.get("lessonName")
		,link = cache.get("link"), form = form)

@app.route('/become_admin', methods=['GET', 'POST'])
@login_required
def become_admin():
	form = AdminCodeForm()
	if form.validate_on_submit():
		# check against the secret in your Config
		if form.admin_code.data == current_app.config['ADMIN_SECRET']:
			current_user.is_admin = True
			db.session.commit()

			# notify Flask-Principal of new role
			identity_changed.send(
				current_app._get_current_object(),
				identity=Identity(current_user.id)
			)

			flash('🎉 You are now an admin! Redirecting…')
			return redirect(url_for('admin.index'))
		else:
			flash('❌ Invalid admin code.', 'error')

	return render_template('become_admin.html', form=form)