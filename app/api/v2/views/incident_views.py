import json
import re
import string
from flask_restplus import Resource
from flask import jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

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
            raise BadRequest("{} is lacking. It is a required field".format(key))
        # validate length
        if key == "description" or key == "location":
            if len(value) < 4:
                raise BadRequest("The {} provided is too short".format(key))

        # if key == "incident_type":
         #   if value != "Red-Flag" or value != "Intervention":
          #      raise BadRequest("{} can only be Red-Flag or Intervention.".format(key))


def _validate_input(req):
    """This function validates the user input and rejects or accepts it"""
    for key, value in req.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))
        elif len(value) < 10:
            raise BadRequest("The {} is too short. Please add more content.".format(key))


@api.route("/")
class Incidents(Resource):
    """This class collects the methods for the auth/signup method"""

    @api.expect(_n_incident, validate=True)
    def post(self):

        _auth = request.headers.get('Authorization')
        if not _auth:
            raise BadRequest("No authorization header provided. This resource is secured.")

        auth_t_oken = _auth.split(" ")[1]
        response = UserModel().decode_auth_token(auth_t_oken)
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
                _incident_saved = incident_model.save_incident()
                if not _incident_saved:

                    raise ValueError

                else:
                    return make_response(jsonify({
                        "Message": "New Incident saved successfully"
                    }), 201)
            except ValueError:
                return make_response(jsonify({"Message": "The incident has already been saved"}))
        else:
            # token is either invalid or expired
            raise Unauthorized("You are not authorized to access this resource.")

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
            raise BadRequest("No authorization header provided. This resource is secured.")

        _auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(_auth_token)
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
            raise Unauthorized("You are not authorized to access this resource.")

    def put(self, incident_id):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest("No authorization header provided. This resource is secured.")

        token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(token)
        if not isinstance(response, str):
            # the token decoded succesfully

            update = request.get_json()
            if not update:
                return make_response(jsonify({"Message": "Provide data in the request"}))

            _validate_input(update)

            _available = IncidentModel().check_item_exists(table="incidents", field="incident_id", data=incident_id)
            if (_available == True):

                updated = update.items()

                for field, data in updated:
                    _table_name = "incidents"
                    IncidentModel().update_item(table=_table_name,
                                                field=field,
                                                data=data,
                                                item_field="incident_id",
                                                item_id=int(incident_id))

                    return make_response(jsonify({
                        "Message": "Tuple updated successfully"
                    }), 201)
            else:
                raise NotFound("Incident")

        else:
            # token is either invalid or expired
            raise Unauthorized("You are not authorized to access this resource.")

    def delete(self, incident_id):

        access_t = request.headers.get('Authorization')
        if not access_t:
            raise BadRequest("No authorization header provided. This resource is secured.")

        auth_ = access_t.split(" ")[1]
        response = UserModel().decode_auth_token(auth_)
        if not isinstance(response, str):
            # the token decoded succesfully

            resp_available = IncidentModel().check_item_exists(table="incidents", field="incident_id", data=incident_id)
            if (resp_available == True):

                tablename = "incidents"

                IncidentModel().delete_item(table_name=tablename, field="incident_id", field_value=incident_id)

                return make_response(jsonify({
                    "Message": "Deleted successfully"
                }), 202)
            else:
                return UserModel().not_found("Incident")

        else:
            # token is either invalid or expired
            raise Unauthorized("You are not authorized to access this resource.")
