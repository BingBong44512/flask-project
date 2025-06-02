from flask import Flask
from config import Config 
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from common import cache

db = SQLAlchemy(app)
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
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Path('/tmp')})
cache.set("subject list", {"astro":[0,0],"bio":[0,0],"chem":[0,0],"physics":[0,0]})

from app import routes
