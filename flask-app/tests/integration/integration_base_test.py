"""
BaseTest

This class is the parent class to each unit test.
It allows to instantiate the database dynamically & makes sure each time
it is a new, blank database.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        with app.app_context():  # loads all the app variables.
            db.init_app(app)
            db.create_all()

        # Get a test client
        self.app = app.test_client()
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
