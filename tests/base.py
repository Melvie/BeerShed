from flask_testing import TestCase

from project import app, db
from project.models import User, CarboyStates


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin", "ad@min.com", "admin", 'guest'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
