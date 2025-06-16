from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config
from app.common import cache
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from random import choice,randint
import json

login_manager = LoginManager()
admin = Admin(template_mode='bootstrap3')


app = Flask(__name__)
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placeholder.db'	

db = SQLAlchemy(app)

login_manager.init_app(app)

from .models import User

admin.add_view(ModelView(User, db.session))
admin.init_app(app)



from app import routes
cache.init_app(app=app, config={"CACHE_TYPE": "SimpleCache"})
cache.set("subjectList", {"astro":[0,-1],"bio":[0,-1],"chem":[0,-1],"physics":[0,-1]})
cache.set("todaySubject","astro")

cache.set("inputText","")
cache.set("correctAnswers",[])

cache.set("lessonName","")
cache.set("link","")


from app import routes

import atexit

from apscheduler.schedulers.background import BackgroundScheduler

def update():
	subjects = cache.get("subjectList")
	cache.set("todaySubject",choice([*subjects.keys()]))
	subjects[cache.get("todaySubject")][1]+=1



	correctAnswers = []
	cache.set("subjectList",subjects)
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
		text1 = text.translate(str.maketrans('', '', """:,.?!"';()"""))
		words = text1.split(" ")
		for word in words:
			if (word in vocab.keys() or (len(word)>7 and randint(0,3)==0)) and word not in correctAnswers:
				xword = "{"+word+", "+choice([*vocab.keys()])+", "+choice([*vocab.keys()])+", "+choice([*vocab.keys()])+"}"
				correctAnswers.append(word)
				text = text.replace(word,xword,1)

	cache.set("inputText",text)
	cache.set("correctAnswers",correctAnswers)



def init_scheduler():
    scheduler = BackgroundScheduler()
    update()
    scheduler.add_job(func=update, trigger="interval", seconds=30)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
