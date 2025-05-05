from flask import Flask, request, jsonify, render_template, redirect,url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

from app import routes