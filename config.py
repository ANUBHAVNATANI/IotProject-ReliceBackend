from os import environ,path
from key import db_uri,db_key

basedir = path.abspath(path.dirname(__file__))

class Config:
    #general config
    FLASK_DEBUG = 1
    FLASK_APP = 'app.py'
    #database config
    SQLALCHEMY_DATABASE_URI = db_uri #environ['DATABASE_URL']
    SECRET_KEY = db_key
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    