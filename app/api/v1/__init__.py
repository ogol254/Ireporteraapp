from .views import Users


from flask_restful import Api, Resource
from flask import Blueprint


version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_one)


api.add_resource(Users, '/users')
