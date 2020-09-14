import os
import flask
import unittest
import tempfile

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, flask.app.config['DATABASE'] = tempfile.mkstemp()
        flask.app.config['TESTING'] = True

