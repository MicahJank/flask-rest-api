import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from configuration.extensions import db
from api import create_app

from models import Video

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

# after creating this file i can run python manager.py db init to create the 
# migrations folder - think 'migrate:make' with knex

# to run the actual migrations run the command python manager.py db migrate