import logging
from flask import Flask, jsonify
from .model import db
from .principal import prin
from .admin import admin
from .api import api

from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object("config")
    app.secret_key = 'NGE0YmQzZjItMDY0Yi00MWE3LThjM2UtNjNmMWM1NzQ4NTI4Cg'
    CORS(app)
    db.init_app(app)
    prin.init_app(api)
    admin.init_app(app, url="/admin")
    app.register_blueprint(api, url_prefix="/api")

    app.logger.setLevel(logging.INFO)
 
    for k, v in app.config.items():
        app.logger.info("{}: {}".format(k ,v))  # pylint: disable=e1101

    return app



