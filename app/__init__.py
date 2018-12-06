from flask import Flask, Blueprint
from instance.config import app_config
from werkzeug.contrib.fixers import ProxyFix


def error_handler(error, message):
    """This function creates a custom dictonary for the error functions"""
    request_data = ""
    if not request.data.decode():
        request_data = "Request body is empty"
    else:
        request_data = json.loads(request.data.decode().replace("'", '"'))

    error_dict = {
        "path_accessed": str(request.path),
        "message": message,
        "request_data": request_data,
        "error": str(error)
    }

    return error_dict


def not_found(error):
    """This function returns a custom JSON response when a resource is not found"""
    message = "The path accessed / resource requested cannot be found, please check"
    error_dict = error_handler(error, message)
    response = make_response(jsonify(error_dict), 404)
    return response


def bad_request(error):
    """This function creates a custom JSON response when a bad request is made"""
    message = "The request made had errors, please check the headers or parameters"
    response = make_response(jsonify(error_handler(error, message)), 400)
    return response


def method_not_allowed(error):
    """This function creates a custom JSON response if the request method is not allowed."""
    message = "The request method used is not allowed"
    return jsonify(error_handler(error, message)), 405


def forbidden(error):
    """Return an error message if the request is forbidden"""
    message = "Sorry, You are not allowed to do that"
    return jsonify(error_handler(error, message)), 403


def unauthorized(error):
    """Unauthorsed access creds"""
    message = "Access denied"
    response = make_response(jsonify(error_handler(error, message)), 401)
    return response


def create_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.wsgi_app = ProxyFix(app.wsgi_app)

    # local imports
    from .api.v1 import version_one as v1
    from .api.v2 import version_two as v2

    app.register_blueprint(v1)
    app.register_blueprint(v2)

    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(403, forbidden)

    return app


app = create_app()
