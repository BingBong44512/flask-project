from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from common import cache

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placeholder.db'
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Path('/tmp')})
cache.set("subject list", {"astro":[0,0],"bio":[0,0],"chem":[0,0],"physics":[0,0]})
db = SQLAlchemy(app)

from app import routes