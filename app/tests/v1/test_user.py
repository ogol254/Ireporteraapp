from ... import create_app
import unittest
import json


app = create_app("testing")


class TestUsers(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = {"name": "john", "email": "email@gmail.com", "password": "12345"}
        self.data2 = {"name": "john", "email": "email@gmai.com", "password": "1235"}

    def test_get(self):
        response = self.app.get('/api/v1/users')
        result = json.loads(response.data)
        self.assertEqual(result["msg"], "success")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.app.post('/api/v1/users', data=json.dumps(self.data), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    def test_redundat_post():
        response = self.app.post('/api/v1/users', data=json.dumps(self.data2), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result["Users"], "User already exist")

    def test_user_edit(self):
        pass


if __name__ == '__main__':
    unittest.main()
