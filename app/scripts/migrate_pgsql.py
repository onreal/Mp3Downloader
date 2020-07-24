from flask_migrate import MigrateCommand
from flask_script import Manager
from app import create_app as app
from app.model.pgsql import User, Session, BotLogger, BotPerson

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
