from flask_restful import Resource
from flask import jsonify, make_response, request

from models import MyFriendsModel


class MyFriends(Resource, MyFriendsModel):
    """docstring for MyFriends"""

    def __init__(self):
        self.db = MyFriendsModel()

    def post(self):
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']

        resp = self.db.save(name, email, password)

        return make_response(jsonify({
            "My new list of friends": resp
        }), 201)

    def get(self):
        resp = self.db.get_friends()
        return make_response(jsonify({
            "My list of friends": resp
        }), 200)
