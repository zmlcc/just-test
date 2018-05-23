from flask import Flask
from .principal import prin
from .model import db
from .main import main
from .admin import admin
from .api import api

from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object("config")
    app.secret_key = 'super-secret-text'
    db.init_app(app)
    admin.init_app(app)
    # prin.init_app(app)
    prin.init_app(api)
    CORS(app)
    app.register_blueprint(main, url_prefix="/testf/")
    app.register_blueprint(api, url_prefix="/testf/zoo/api")

    return app

