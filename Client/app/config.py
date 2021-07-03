import sys
import os
from dotenv import load_dotenv, find_dotenv

from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(find_dotenv())

class BaseConfig(object):
    DEBUG = True
    use_reloader=True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my super secret key"