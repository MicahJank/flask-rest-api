from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# grabs whatever the root of the project directory is, note that this must be in a root level file
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.py') # i can use this anywhere to access the config path root
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class Production(Config):
    DATABASE_URI_PROD = os.environ.get("DATABASE_URI_PROD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEVELOPMENT = True

class Testing(Config):
    TESTING = True

# this function will return the environment flask should run it, ultimately that will be determined by an env variable
# defaults to development if nothing is supplied
def getConfig(environment="development"):
    if environment == 'production':
        return Production
    elif environment == 'testing':
        return Testing
    else:
        return Development





# # initialize the database (note that sqlalchemy uses sqlite for storage)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# db = SQLAlchemy(app)