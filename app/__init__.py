from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import routes
from app.models import *

# 在login = LoginManager(app)后面加上即可
login.login_view = 'login'