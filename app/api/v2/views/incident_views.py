import json
import re
import string
from flask_restplus import Resource
from flask import jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash

from ..models.auth_models import UserModel
from ..models.incidence_models import IncidentModel
from ..models.comment_models import CommentModel
from ..utils.serializers import IncidentDTO

api = IncidentDTO().api
_n_incident = IncidentDTO().n_incident


def _validate_incident(incident):
    """This function validates the user input and rejects or accepts it"""
    for key, value in incident.items():
        # ensure keys have values
        if not value:
            return make_response(jsonify({
                "Message": "{} is lacking. It is a required field".format(key)
            }), 400)
        # validate length
        if key == "description" or key == "location":
            if len(value) < 4:
                return make_response(jsonify({
                    "Message": "The {} provided is too short".format(key)
                }), 400)

        # if key == "type":
            # if value not "Red-Flag" or "Intervention":
                # return("{} can only be Red-Flag or Intervention.".format(key))


def _validate_input(req):
    """This function validates the user input and rejects or accepts it"""
    for key, value in req.items():
        # ensure keys have values
        if not value:
            return("{} is lacking. It is a required field".format(key))
        elif len(value) < 10:
            return("The {} is too short. Please add more content.".format(key))


@api.route("/")
class Incidents(Resource):
    """This class collects the methods for the auth/signup method"""

    @api.expect(_n_incident, validate=True)
    def post(self):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response(jsonify({
                "Message": "No authorization header provided. This resource is secured."
            }), 400)

        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully
            user_id = response
            req_data = request.data.decode().replace("'", '"')
            if not req_data:
                return make_response(jsonify({"Message": "Provide data in the request"}))
            incident_req_data = json.loads(req_data)
            try:
                description = incident_req_data['description'].strip()
                location = incident_req_data['location'].strip()
                typee = incident_req_data['incident_type'].strip()
            except (KeyError, IndexError) as e:
                return(e)
            new_incident = {
                "created_by": user_id,
                "description": description,
                "incident_type": typee,
                "location": location,
                "status": "Pending"
            }
            _validate_incident(new_incident)
            incident_model = IncidentModel(**new_incident)
            try:
                saved = incident_model.save_incident()
                if not saved:
                    raise ValueError
                else:
                    return make_response(jsonify({
                        "Message": "New Incident saved successfully"
                    }), 201)
            except ValueError:
                return make_response(jsonify({"Message": "The incident has already been saved"}))
        else:
            # token is either invalid or expired
            return make_response(jsonify({
                "Message": "You are not authorized to access this resource."
            }), 401)

    def get(self):
        """This endpoint allows a registered user to post a question."""
        # get questions from db
        incidents = IncidentModel().get_all_incidents()
        resp = {
            "message": "success",
            "Incidents": incidents
        }
        return resp, 200


@api.route("/<int:incident_id>")
class GetIncidents(Resource):
    """This class collects the methods for the auth/signup method"""

    def get(self, incident_id):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response(jsonify({
                "Message": "No authorization header provided. This resource is secured."
            }), 400)

        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully
            incident = IncidentModel().get_specific_incident(incident_id)
            comments = CommentModel().get_all_comments_by_incident(incident_id)
            if not comments:
                comments = "No comments yet"

            resp = {
                "message": "success",
                "Incident": incident,
                "Comments": {
                    "comments": comments
                }
            }
            return resp, 200
        else:
            # token is either invalid or expired
            return make_response(jsonify({
                "Message": "You are not authorized to access this resource."
            }), 401)

    def put(self, incident_id):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response(jsonify({
                "Message": "No authorization header provided. This resource is secured."
            }), 400)

        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully

            update = request.get_json()
            if not update:
                return make_response(jsonify({"Message": "Provide data in the request"}))

            _validate_input(update)

            exists = IncidentModel().check_item_exists(table="incidents", field="incident_id", data=incident_id)
            if (exists == True):

                updated = update.items()

                for field, data in updated:
                    table = "incidents"
                    item_field = "incident_id"
                    IncidentModel().update_item(table=table,
                                                field=field,
                                                data=data,
                                                item_field=item_field,
                                                item_id=int(incident_id))

                    return make_response(jsonify({
                        "Message": "Updated successfully"
                    }), 201)
            else:
                return make_response(jsonify({
                    "Message": "Incident not found"
                }), 404)

        else:
            # token is either invalid or expired
            return make_response(jsonify({
                "Message": "You are not authorized to access this resource."
            }), 401)

    def delete(self, incident_id):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response(jsonify({
                "Message": "No authorization header provided. This resource is secured."
            }), 400)

        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully

            exists = IncidentModel().check_item_exists(table="incidents", field="incident_id", data=incident_id)
            if (exists == True):

                table_name = "incidents"
                field = 'incident_id'

                IncidentModel().delete_item(table_name=table_name, field=field, field_value=incident_id)

                return make_response(jsonify({
                    "Message": "Deleted successfully"
                }), 200)
            else:
                return make_response(jsonify({
                    "Message": "Incident not found"
                }), 404)

        else:
            # token is either invalid or expired
            return make_response(jsonify({
                "Message": "You are not authorized to access this resource."
            }), 401)
