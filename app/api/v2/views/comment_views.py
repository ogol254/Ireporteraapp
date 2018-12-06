import json
import re
import string
from flask_restplus import Resource
from flask import jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash

from ..models.auth_models import UserModel
from ..models.comment_models import CommentModel
from ..utils.serializers import CommentDTO

api = CommentDTO().api
_n_comment = CommentDTO().n_comment


@api.route("/")
class Comments(Resource):
    """This class collects the methods for the auth/signup method"""

    @api.expect(_n_comment, validate=True)
    def post(self):

        head_t = request.headers.get('Authorization')
        if not head_t:
            return UserModel().badrequest()

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
            comment_model = CommentModel(**new_comment)
            try:
                saved = comment_model.save_comment()
                if not saved:
                    raise ValueError
                else:
                    return make_response(jsonify({
                        "Message": saved
                    }), 201)
            except ValueError:
                return make_response(jsonify({"Message": "The comment has already been saved"}))
        else:
            # token is either invalid or expired
            return UserModel().unauthorized()


@api.route("/<int:comment_id>")
class GetComment(Resource):
    """This class collects the methods for the auth/signup method"""

    def put(self, comment_id):

        t_header = request.headers.get('Authorization')
        if not t_header:
            return UserModel().badrequest()

        auth_token = t_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully

            update = request.get_json()
            if not update:
                return make_response(jsonify({"Message": "Provide data in the request"}))

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
                    }), 201)
            else:
                return UserModel().not_found("Comment")

        else:
            # token is either invalid or expired
            return UserModel().unauthorized()

    def delete(self, comment_id):

        header_token = request.headers.get('Authorization')
        if not header_token:
            return UserModel().badrequest()

        auth_token = header_token.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully

            exist_s = CommentModel().check_item_exists(table="comments", field="comment_id", data=comment_id)
            if (exist_s == True):
                table_ = "comments"

                CommentModel().delete_item(table_name=table_, field="comment_id", field_value=comment_id)

                return make_response(jsonify({
                    "Message": "Deleted successfully"
                }), 200)
            else:
                return UserModel().not_found("Comment")

        else:
            # token is either invalid or expired
            return UserModel().unauthorized()
