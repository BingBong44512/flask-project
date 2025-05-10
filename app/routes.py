from flask import Flask, request, jsonify, render_template, redirect,url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app import app

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=["POST","GET"])
def login():
	return render_template('login.html')