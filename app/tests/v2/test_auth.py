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
from ...db_config import init_test_db
from ...db_config import destroy


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

    def user_login(self):
        """Test that a user can login using a POST request"""
        self.post_data(data=self.user)
        payload = {
            "username": self.user['username'],
            "password": self.user['password']
        }
        # attempt to log in
        login = self.post_data('/api/v2/auth/signin', data=payload)
        result = json.loads(login.data)
        token = result['access-token']
        return token

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
        result = json.loads(new_user.data)
        # test that the server responds with the correct status code
        self.assertEqual(new_user.status_code, 201)
        #self.assertEqual(result["Message"], "The username already exists")

    def test_user_login(self):
        """Test that a user can login using a POST request"""
        self.post_data(data=self.user)
        payload = {
            "username": self.user['username'],
            "password": self.user['password']
        }
        # attempt to log in
        login = self.post_data('/api/v2/auth/signin', data=payload)
        result = json.loads(login.data)
        self.assertEqual(result["Message"], "Success")
        self.assertEqual(login.status_code, 201)
        self.assertTrue(result["access-token"])

    def test_user_logout(self):
        """Test that the user can logout using a POST request"""
        new_user = self.user_login()
        path = "/api/v2/auth/signout"
        token = new_user
        headers = {"Authorization": "Bearer {}".format(token)}
        logout = self.client.post(path=path,
                                  headers=headers,
                                  content_type="application/json")
        self.assertEqual(logout.status_code, 200)
        logout_again = self.client.post(path=path,
                                        headers=headers,
                                        content_type="application/json")
        self.assertEqual(logout_again.status_code, 401)

    def test_an_unregistered_user(self):
        """Test that an unregistered user cannot log in"""
        # generate random username and password
        un_user = {
            "username": "".join(choice(
                                string.ascii_letters) for x in range(randint(7, 10))),
            "passsword": "".join(choice(
                string.ascii_letters) for x in range(randint(7, 10))),
        }
        # attempt to log in
        login = self.post_data('/api/v2/auth/signin', data=un_user)
        self.assertEqual(login.status_code, 400)

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
