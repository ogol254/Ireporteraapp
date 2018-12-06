"""
This module tests the incidents end point
"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app

from ...db_config import init_test_db
from ...db_config import destroy


class TestQuestions(unittest.TestCase):
    """This class collects all the test cases for the incidents"""

    def create_user(self):
        """create a fictitious user"""
        username = "".join(choice(
                           string.ascii_letters) for x in range(randint(7, 10)))
        params = {
            "first_name": "ugali",
            "last_name": "mayai",
            "email": "ugalimayai@gmail.com",
            "username": "username",
            "password": "password"
        }
        path = "/api/v2/auth/signup"
        reg = self.client.post(path,
                               data=json.dumps(params),
                               content_type="application/json")

        payload = {
            "username": params['username'],
            "password": params['password']
        }
        path = "/api/v2/auth/signin"
        user = self.client.post(path,
                                data=json.dumps(payload),
                                content_type="application/json")
        token = user.json['access-token']
        user_id = user.json['username']
        return user_id, token

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.incident = {
            "location": "Nairobi",
            "description": "Corruption case",
            "incident_type": "Red-Flag"
        }
        self.comment = {
            "comment": "The matter is under investigation",
            "incident_id": 1
        }
        with self.app.app_context():
            self.db = init_test_db()

    def post_data_incident(self, path='/api/v2/incidents', auth_token=2, data={}, headers=0):
        """This function performs a POST request using the testing client"""
        if not data:
            data = self.incident
        if auth_token is 2:
            user = self.create_user()
            auth_token = user[1]
        if not headers:
            headers = {"Authorization": "Bearer {}".format(auth_token)}
        result = self.client.post(path, data=json.dumps(data),
                                  headers=headers,
                                  content_type='application/json')
        return result

    def post_data_comment(self, path='/api/v2/incident/comment', auth_token=2, data={}, headers=0):
        """This function performs a POST request using the testing client"""
        if not data:
            data = self.comment
        if auth_token is 2:
            user = self.create_user()
            auth_token = user[1]
        if not headers:
            headers = {"Authorization": "Bearer {}".format(auth_token)}
        result = self.client.post(path, data=json.dumps(data),
                                  headers=headers,
                                  content_type='application/json')
        return result

    def get_data(self, path='/api/v2/incident/comment'):
        """This function performs a GET request to a given path
            using the testing client
        """
        result = self.client.get(path)
        return result

    def test_post_comment(self):
        """Test that a user can post a comment
        """
        new_incident = self.post_data_incident()
        new_comment = self.post_data_comment()
        # test that the server responds with the correct status code
        self.assertEqual(new_comment.status_code, 201)
        self.assertTrue(new_comment.json['Message'])

    def test_post_comment_without_incident(self):
        """Test that a user can post a comment
        """
        new_comment = self.post_data_comment()
        # test that the server responds with the correct status code
        self.assertEqual(new_comment.status_code, 201)
        self.assertTrue(new_comment.json['Message'])
        self.assertEqual(new_comment.json['Message'], "The incident you are trying to comment is not found")

    def test_unauthorized_request(self):
        """Test that the endpoint rejects unauthorized requests"""
        # test false token
        false_token = self.post_data_comment(headers=dict(Authorization="Bearer wrongtoken"))
        self.assertEqual(false_token.status_code, 401)
        # test correct token
        correct_token = self.post_data_incident()
        self.assertEqual(correct_token.status_code, 201)

    def tearDown(self):
        """This function destroys items created during the test run"""
        with self.app.app_context():
            destroy()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
