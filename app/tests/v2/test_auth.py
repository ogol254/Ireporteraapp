"""
This module tests the authentication endpoint
Authored by: ogol
"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app
from ...db_config import destroy
from ...db_config import init_test_db


class AuthTest(unittest.TestCase):
    """This class collects all the test cases for the users"""

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user = {
            "first_name": "ugali",
            "last_name": "mayai",
            "email": "testemail@gmail.com",
            "username": "testuser",
            "password": "password"
        }
        self.error_msg = "The path accessed / resource requested cannot be found, please check"

        with self.app.app_context():
            self.db = init_test_db()

    def post_data(self, path='/api/v2/auth/signup', data={}):
        """This function performs a POST request using the testing client"""
        if not data:
            data = self.user
        result = self.client.post(path, data=json.dumps(data),
                                  content_type='application/json')
        return result

    def get_data(self, path):
        """This function performs a GET request to a given path
            using the testing client
        """
        result = self.client.get(path)
        return result

    def test_sign_up_user(self):
        """Test that a new user can sign up using a POST request
        """
        new_user = self.post_data(data=self.user)
        # test that the server responds with the correct status code
        self.assertEqual(new_user.status_code, 201)

    def test_user_login(self):
        """Test that a user can login using a POST request"""
        self.post_data(data=self.user)
        payload = dict(
            username=self.user['username'],
            password=self.user['password']
        )
        # attempt to log in
        login = self.post_data('/api/v2/auth/signin', data=payload)
        self.assertEqual(login.json["Message"], "Success")

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
