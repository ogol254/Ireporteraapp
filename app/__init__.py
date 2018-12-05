from flask import Flask, Blueprint
from instance.config import app_config
from werkzeug.contrib.fixers import ProxyFix

# local imports
from .api.v1 import version_one as v1
from .api.v2 import version_two as v2


def create_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.register_blueprint(v1)
    app.register_blueprint(v2)
    return app


app = create_app()
