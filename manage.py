# manage.py

# Manager class keeps track of all the commands and handles how they are called from the command line. 
# The MigrateCommand contains a set of migration commands. We've also imported the models so that 
# the script can find the models to be migrated. The manager also adds the migration commands 
# and enforces that they start with db

# python manage.py db init
# python manage.py db migrate # alembic auto generate the model
# python manage.py db upgrade

import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models


app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()