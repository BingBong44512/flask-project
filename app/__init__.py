from flask import Flask
from config import Config
from app.common import cache
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placeholder.db'
cache.init_app(app=app, config={"CACHE_TYPE": "SimpleCache"})
cache.set("subjectList", {"astro":[0,-1],"bio":[0,-1],"chem":[0,-1],"physics":[0,-1]})
cache.set("todaySubject","astro")
db = SQLAlchemy(app)

from app import routes

import atexit

from apscheduler.schedulers.background import BackgroundScheduler

def update():
	subjects = cache.get("subjectList")
	cache.set("todaySubject",choice([*subjects.keys()]))
	subjects[cache.get("todaySubject")][1]+=1
	cache.set("subjectList",subjects)


def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update, trigger="interval", seconds=5)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())