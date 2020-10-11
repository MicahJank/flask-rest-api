from flask import Flask, Blueprint
from  configuration.config import CONFIG_PATH, Development
from configuration.extensions import db
from dotenv import load_dotenv
import os


print(Development())
print(os.environ.get("DATABASE_URL"))
def create_app():
    app = Flask(__name__)
    app.config.from_object()

    db.init_app(app)


    # register blueprints here


    return app