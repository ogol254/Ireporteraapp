from flask_restful import Resource
from flask import jsonify, make_response, request

from .models import UsersModel


class Users(Resource, UsersModel):
    """docstring for MyFriends"""

    def __init__(self):
        self.db = UsersModel()

    def post(self):
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']

        resp = self.db.save(name, email, password)

        return make_response(jsonify({
            "Users": resp
        }), 201)

    def get(self):
        resp = self.db.get_friends()
        return make_response(jsonify({
            "Users": resp,
            "msg": "success"
        }), 200)
