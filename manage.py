# -*- coding: UTF-8 -*-

import os

from app import create_app, db
from app.models import User, Department, Comment, Gem, Team, Draft, Proposal
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('GEMS_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(
        app=app, db=db, User=User, Dep=Department, Comment=Comment, Team=Team,
        Gem=Gem, Draft=Draft, Proposal=Proposal
    )

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def initialize_database():
    """Initialize new DB."""
    db.drop_all()
    db.create_all()
    print("New database initialized.")

@manager.command
def generate_fake():
    """Generate fake data."""
    Department.generate_fake()
    User.generate_fake()
    Draft.generate_fake()
    print("Generating fake data complete.")

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    
    # upgrade database to the latest model
    upgrade()


if __name__ == '__main__':
    manager.run()
