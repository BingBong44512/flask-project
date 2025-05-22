from flask import Flask
from config import Config 
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(template_mode='bootstrap3')


app = Flask(__name__)
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placeholder.db'	

db.init_app(app)
login_manager.init_app(app)
admin.init_app(app)

from .models import User

admin.add_view(ModelView(User, db.session))

from app import routes