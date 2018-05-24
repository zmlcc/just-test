from flask import Flask
from .principal import prin
from .model import db
from .admin import admin
from .api import api

from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object("config")
    app.secret_key = 'NGE0YmQzZjItMDY0Yi00MWE3LThjM2UtNjNmMWM1NzQ4NTI4Cg'
    CORS(app)
    db.init_app(app)
    admin.init_app(app, url="/admin")
    app.register_blueprint(api, url_prefix="/api")

    prin.init_app(api)
    prin.init_app(admin)

    return app

