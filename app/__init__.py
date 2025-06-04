from flask import Flask
from config import Config
from app.common import cache
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placeholder.db'
cache.init_app(app=app, config={"CACHE_TYPE": "SimpleCache"})
cache.set("subject list", {"astro":[0,0],"bio":[0,0],"chem":[0,0],"physics":[0,0]})
cache.set("todaySubject","astro")
db = SQLAlchemy(app)

from app import routes