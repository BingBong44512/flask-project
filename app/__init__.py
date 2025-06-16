from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config
from app.common import cache
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from random import choice,randint
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, identity_loaded, UserNeed, RoleNeed, Permission
import json
from flask_mailman import Mail
import re
from random import sample, shuffle

login_manager = LoginManager()
admin = Admin(template_mode='bootstrap3')


app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placeholder.db'	
db = SQLAlchemy(app)

login_manager.init_app(app)

mail = Mail(app)

principals = Principal(app)

# define a global “admin” permission
admin_permission = Permission(RoleNeed('admin'))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
	# attach the User object to the identity
	identity.user = current_user

	# every logged in user gets a UserNeed
	if not current_user.is_anonymous:
		identity.provides.add(UserNeed(current_user.id))

	# and if they have is_admin, give them the “admin” RoleNeed
	if getattr(current_user, 'is_admin', False):
		identity.provides.add(RoleNeed('admin'))

from flask_admin.contrib.sqla import ModelView
from flask import redirect, request

class AdminOnlyModelView(ModelView):
    def is_accessible(self):
        return admin_permission.can()
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if not allowed
        return redirect(url_for('login', next=request.url))

migrate = Migrate(app, db)

from .models import User

admin.add_view(AdminOnlyModelView(User, db.session))
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

	def replace_once_whole_word(text, word, placeholder):
		pattern = r'\b' + re.escape(word) + r'\b'
		return re.sub(pattern, placeholder, text, count=1)

	for word in words:
		if (word in vocab or (len(word) > 7 and randint(0,3) == 0)) and word not in correctAnswers:
			# 1. pick 3 distractors
			distractors = sample([w for w in vocab if w != word], 3)
			# 2. build & shuffle options
			options = [word] + distractors
			shuffle(options)
			# 3. turn into your {…} placeholder
			xword = "{" + ", ".join(options) + "}"

			correctAnswers.append(word)
			# 4. replace *only* the first exact match
			text = replace_once_whole_word(text, word, xword)

	cache.set("inputText",text)
	cache.set("correctAnswers",correctAnswers)



def init_scheduler():
	scheduler = BackgroundScheduler()
	try:
		update()
	except Exception as e:
		print(f"Initial update failed: {e}")
	scheduler.add_job(func=update, trigger="interval", seconds=10)
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())
