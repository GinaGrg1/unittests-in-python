from unittest import TestCase
from app import app


class BaseTest(TestCase):
    def setUp(self) -> None:
        """
        Note that if you are testing for assertions or exceptions in your
        application code, you must set ``app.testing = True`` in order for the
        exceptions to propagate to the test client.  Otherwise, the exception
        will be handled by the application (not visible to the test client) and
        the only indication of an AssertionError or other exception will be a
        500 status code response to the test client.  See the :attr:`testing`
        attribute.  For example::

        app.testing = True
        client = app.test_client()

        """
        app.testing = True
        self.app = app.test_client()
