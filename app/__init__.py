from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placeholder.db'
db = SQLAlchemy(app)

from app import routes

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
        app.run(host="0.0.0.0", port=8080)
