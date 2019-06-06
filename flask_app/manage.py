#!/usr/bin/env python3
"""Manage Script."""

import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from digital_lotus import app, db
from digital_lotus.models import User


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Run the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='digital_lotus/*')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()


@manager.command
def create_db():
    """Create the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drop the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Create the admin user."""
    db.session.add(
        User(username="admin",
             first_name='Admin',
             last_name='Admin',
             email="admin@test.com",
             password="admin",
             admin=True)
    )
    db.session.commit()


if __name__ == '__main__':
    manager.run()
