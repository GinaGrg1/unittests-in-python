"""
BaseTest

This class is the parent class to each unit test.
It allows to instantiate the database dynamically & makes sure each time
it is a new, blank database.

setUpClass is run once for the whole class.
setUp is run before & after each test method.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    @classmethod
    def setUpClass(cls) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = BaseTest.SQLALCHEMY_DATABASE_URI
        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True  # Bottle ups the errors expected in tests.
        with app.app_context():  # loads all the app variables.
            db.init_app(app)

    def setUp(self):
        # Get a test client
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
