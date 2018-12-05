from flask_restplus import Api
from flask import Blueprint

version_two = Blueprint('api_v2', __name__, url_prefix='/api/v2')

from .views.auth_views import api as auth_ns
from .views.incident_views import api as incidence_ns
from .views.comment_views import api as comment_ns

api = Api(version_two,
          title='Ireporter',
          version='2.0',
          description="an app for reaising incidences")

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(incidence_ns, path="/incidents")
api.add_namespace(comment_ns, path="/incident/comment")
