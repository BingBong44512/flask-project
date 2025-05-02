from flask import Flask, request, jsonify, render_template, redirect,url_for, session

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
