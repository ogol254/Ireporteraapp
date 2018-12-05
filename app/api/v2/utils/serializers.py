"""
This module collects all the Data Transfer Objects for the API
"""
from flask_restplus import Namespace, fields


class UserDTO(object):
    """User Data Transfer Object"""
    api = Namespace('auth', description='user authentication and signup resources')
    n_user = api.model('new user request', {
        'first_name': fields.String(required=True, description="user's first name"),
        'last_name': fields.String(required=True, description="user's last name"),
        'username': fields.String(required=True, description="user's username"),
        'email': fields.String(required=True, description="user's email address"),
        'password': fields.String(required=True, description="user's password")
    })
    user = api.model('login request', {
        'username': fields.String(required=True, description="user's username"),
        'password': fields.String(required=True, description="user's password")
    })


class IncidentDTO(object):
    """incident Data Transfer Object"""
    api = Namespace('incident', description='Incidents Proceses')
    n_incident = api.model('new incident post  request', {
        'description': fields.String(required=True, description="description of the incident"),
        'location': fields.String(required=True, description="location"),
        'incident_type': fields.String(required=True, description="type of the incident"),
    })


class CommentDTO(object):
    """docstring for comments posting"""
    api = Namespace('comment', description='comments Proceses')
    n_comment = api.model('new comment post  request', {
        'comment': fields.String(required=True, description="description of the comment"),
        'incident_id': fields.Integer(required=True, description="incident_id")
    })
