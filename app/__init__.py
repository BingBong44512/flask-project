from flask import Flask
from config import Config
from app.common import cache
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from random import choice
import json 
import os

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placeholder.db'
cache.init_app(app=app, config={"CACHE_TYPE": "SimpleCache"})
cache.set("subjectList", {"astro":[0,-1],"bio":[0,-1],"chem":[0,-1],"physics":[0,-1]})
cache.set("todaySubject","astro")

cache.set("inputText","")
cache.set("correctAnswers",[])

cache.set("lessonName","")
cache.set("link","")

db = SQLAlchemy(app)

from app import routes

import atexit

from apscheduler.schedulers.background import BackgroundScheduler

def update():
	subjects = cache.get("subjectList")
	cache.set("todaySubject",choice([*subjects.keys()]))
	subjects[cache.get("todaySubject")][1]+=1



	correctAnswers = []
	inputText = ""

	subject = cache.get("todaySubject")
	lessonNum = cache.get("subjectList")[subject]
	text = ""

	with open('app/static/content/'+subject+"content.json", 'r') as utext:
		content= json.load(utext)
		chapterDict = content[[*content.keys()][lessonNum[0]]]

		if len(chapterDict)-1<lessonNum[1]:
			lessonNum[0]+=1
			lessonNum[1]=0
			subjects[cache.get("todaySubject")]=lessonNum
			cache.set("subjectList",subjects)


		chapterDict = content[[*content.keys()][lessonNum[0]]]
		currentText = chapterDict[[*chapterDict.keys()][lessonNum[1]]]
		cache.set("lessonName",[*chapterDict.keys()][lessonNum[1]])
		cache.set("link",currentText["link"])
		text = currentText["content"]

	with open('app/static/dicts/'+subject+"dict.json", 'r') as uvocab:
		vocab = json.load(uvocab)
		words = text.split(" ")
		for word in words:
			word = word.remove()



def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update, trigger="interval", seconds=5)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())