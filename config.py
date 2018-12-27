import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'dji390dsa0HD$jkf3d#odj'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Miku0831@localhost:3306/flaskblog?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False