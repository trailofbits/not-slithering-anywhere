import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./app.db'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
