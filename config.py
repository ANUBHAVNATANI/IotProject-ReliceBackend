from os import environ,path

basedir = path.abspath(path.dirname(__file__))

class Config:
    #general config
    FLASK_DEBUG = 1
    FLASK_APP = 'app.py'
    #database config
    SQLALCHEMY_DATABASE_URI = ''
    