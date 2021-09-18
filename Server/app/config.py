import sys
import os
from dotenv import load_dotenv, find_dotenv

from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(find_dotenv())

class BaseConfig(object):
    DEBUG = True
    use_reloader=True
    
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv("DB_PASS")
    DB_SERVICE = os.getenv("DB_SERVICE")
    DB_PORT = os.getenv("DB_PORT")
    
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASS}@{DB_SERVICE}:{DB_PORT}/{DB_NAME}'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pricepred.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my super secret key"