import json
import re
import string
from flask_restplus import Resource
from flask import jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from ..models.auth_models import UserModel
from ..models.comment_models import CommentModel
from ..utils.serializers import CommentDTO

api = CommentDTO().api
_n_comment = CommentDTO().n_comment


def _validate_input(req):
    """This function validates the user input and rejects or accepts it"""
    for key, value in req.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))

        if key == "comment":
            if len(value) < 5:
                raise BadRequest("The {} provided is too short".format(key))


@api.route("/")
class Comments(Resource):
    """This class collects the methods for the auth/signup method"""

    @api.expect(_n_comment, validate=True)
    def post(self):

        head_t = request.headers.get('Authorization')
        if not head_t:
            raise BadRequest("No authorization header provided. This resource is secured.")

        auth_token = head_t.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully
            username = response
            req_data = request.data.decode().replace("'", '"')
            if not req_data:
                return make_response(jsonify({"Message": "Provide data in the request"}))
            comment_req_data = json.loads(req_data)
            try:
                comment = comment_req_data['comment'].strip()
                incident_id = int(comment_req_data['incident_id'])
            except (KeyError, IndexError) as e:
                return(e)
            new_comment = {
                "created_by": username,
                "incident_id": incident_id,
                "comment": comment
            }
            _validate_input(new_comment)

            in_exist = CommentModel().check_item_exists(table="incidents", field="incident_id", data=new_comment['incident_id'])
            if (in_exist == True):
                comment_model = CommentModel(**new_comment)
                c_omment = comment_model.save_comment()
                try:
                    if not c_omment:
                        raise ValueError
                    else:
                        return make_response(jsonify({
                            "Message": "New comment saved successfully",
                            "comment_id": c_omment
                        }), 201)

                except ValueError:
                    return make_response(jsonify({"Message": "The comment has already been saved"}))
            else:
                return make_response(jsonify({
                    "Message": "The incident you are trying to comment is not found"
                }), 201)

        else:
            # token is either invalid or expired
            raise Unauthorized("You are not authorized to access this resource.")


@api.route("/<int:comment_id>")
class GetComment(Resource):
    """This class collects the methods for the auth/signup method"""

    def put(self, comment_id):

        t_header = request.headers.get('Authorization')
        if not t_header:
            raise BadRequest("No authorization header provided. This resource is secured.")

        auth_token = t_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully

            update = request.get_json()
            if not update:
                return make_response(jsonify({"Message": "Provide data in the request"}))

            _validate_input(update)

            _exists = CommentModel().check_item_exists(table="comments", field="comment_id", data=comment_id)
            if _exists == True:

                updated = update.items()

                for field, data in updated:
                    table_name = "comments"
                    item_field = "comment_id"
                    CommentModel().update_item(table=table_name,
                                               field=field,
                                               data=data,
                                               item_field=item_field,
                                               item_id=int(comment_id))

                    return make_response(jsonify({
                        "Message": "{} updated successfully".format(field)
                    }), 202)
            else:
                raise NotFound("Comment not found")

        else:
            # token is either invalid or expired
            raise Unauthorized("You are not authorized to access this resource.")

    def delete(self, comment_id):

        _h_ = request.headers.get('Authorization')
        if _h_:

            auth_token = _h_.split(" ")[1]
            response = UserModel().decode_auth_token(auth_token)
            if not isinstance(response, str):
                # the token decoded succesfully

                exist_s = CommentModel().check_item_exists(table="comments", field="comment_id", data=comment_id)
                if (exist_s == False):
                    raise NotFound("Comment not found")

                else:
                    CommentModel().delete_item(table_name="comments", field="comment_id", field_value=comment_id)
                    return make_response(jsonify({
                        "Message": "Deleted successfully"
                    }), 202)

            else:
                # token is either invalid or expired
                raise Unauthorized("You are not authorized to access this resource.")
        else:
            raise BadRequest("No authorization header provided. This resource is secured.")
