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


class SingleUser(Resource, UsersModel):
    """docstring for SingleUser"""

    def __init__(self):
        self.user = UsersModel()

    def get(self, id):
        resp = self.user.get_single_user(id)
        return make_response(jsonify({
            "Users": resp,
            "msg": "success"
        }), 200)

    def put(sel, id):
        pass

    def delete(self, id):
        pass
