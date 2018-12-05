from flask_restplus import Resource
from flask import jsonify, make_response, request
import json
import re
import string
from werkzeug.security import generate_password_hash, check_password_hash

from ..models.auth_models import UserModel
from ..utils.serializers import UserDTO

api = UserDTO().api
_n_user = UserDTO().n_user
login_user = UserDTO().user


def _validate_user(user):
    """This function validates the user input and rejects or accepts it"""
    for key, value in user.items():
        # ensure keys have values
        if not value:
            return("{} is lacking. It is a required field".format(key))
        # validate length
        if key == "username" or key == "password":
            if len(value) < 5:
                return("The {} provided is too short".format(key))
            elif len(value) > 15:
                return("The {} provided is too long".format(key))
        if key == "first_name" or key == "last_name" or key == "username":
            for i in value:
                if i not in string.ascii_letters:
                    return("{} cannot have non-alphabetic characters.".format(key))


@api.route("/signup")
class AuthSignup(Resource):
    """This class collects the methods for the auth/signup method"""

    @api.expect(_n_user, validate=True)
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            return make_response(jsonify({"Message": "Provide data in the request"}))
        user_details = json.loads(req_data)
        try:
            username = user_details['username'].strip()
            first_name = user_details['first_name'].strip()
            last_name = user_details['last_name'].strip()
            email = user_details['email'].strip()
            password = user_details['password'].strip()
            if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                            email):
                return make_response(jsonify({"Message": "The email provided is invalid"}))
        except (KeyError, IndexError) as e:
            return()
        user = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        _validate_user(user)
        user_model = UserModel(**user)
        try:
            saved = user_model.save_user()
            if not saved:
                raise ValueError
            else:
                return make_response(jsonify({
                    "Message": saved
                }), 201)
        except ValueError:
            return make_response(jsonify({"Message": "The username already exists"}))


@api.route("/signin")
class AuthLogin(Resource):
    """This class collects the methods for the auth/signup method"""

    @api.expect(login_user, validate=True)
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            return make_response(jsonify({"Message": "Provide data in the request"}))
        login_details = json.loads(req_data)
        username = login_details['username'].strip()
        password = login_details['password'].strip()

        login_data = {
            "username": username,
            "password": password
        }

        _validate_user(login_data)

        user = UserModel(**login_data)
        record = user.get_user_by_username(username)
        if not record:
            return make_response(jsonify({
                "Message": "Your details were not found, please sign up"
            }), 401)

        user_id, first_name, last_name, passwordharsh, username = record
        if not check_password_hash(passwordharsh, password):
            return make_response(jsonify({
                "Message": "Username and Password do not match"
            }), 401)

        token = user.encode_auth_token(username)

        return make_response(jsonify({
            "Message": "Success",
            "access-token": token
        }), 201)


@api.route('/signout')
class AuthLogout(Resource):
    """This class collects the methods for the  endpoint"""

    def post(self):
        """This endpoint allows a registered user to logout."""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response(jsonify({
                "Message": "No authorization header provided. This resource is secured."
            }), 400)
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            # token is either invalid or expired
            return make_response(jsonify({
                "Message": "You are not authorized to access this resource. {}".format(response)
            }), 401)
        else:
            # the token decoded succesfully
            # logout the user
            user_token=UserModel().logout_user(auth_token)
            resp=dict()
            return {"message": "logout successful. {}".format(user_token)}, 200
