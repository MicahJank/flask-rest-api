# the main part of the api where everything gets connected to
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configuration.extensions import db
from configuration.config import getConfig
from dotenv import load_dotenv
import os

load_dotenv()
# loads the environment depending on what is supplied to the environment variable
environment = getConfig(os.environ.get('FLASK_ENV'))
# creates the flask app
app = Flask(__name__)

app.config.from_object(environment)

db.init_app(app)


# creates the database - models should be defined before this is called
if os.path.exists('database.db') == False:
    # create_all should only be called if there is no database already created, this is why i check to see
    # if the file exists first
    db.create_all()

if __name__ == "__index__":
    app.run(debug=True)