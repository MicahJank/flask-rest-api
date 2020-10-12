from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from configuration.config import getConfig
from configuration.extensions import db
import models
from dotenv import load_dotenv
import os


load_dotenv()
def create_app():
    # loads the environment depending on what is supplied to the environment variable
    environment = getConfig(os.environ.get('FLASK_ENV'))
    # creates the flask app
    app = Flask(__name__)

    # initializes the flask app as an API
    api = Api(app)

    app.config.from_object(environment)
    
    db.init_app(app)



    # register blueprints here

    # creates the database - models should be defined before this is called
    if os.path.exists('database.db') == False:
        # create_all should only be called if there is no database already created, this is why i check to see
        # if the file exists first
        db.create_all()

    return app