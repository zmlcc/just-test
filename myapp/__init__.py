from flask import Flask
from .model import db
from .main import main
from .admin import admin


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object("config")
    app.secret_key = 'super-secret-text'
    db.init_app(app)
    admin.init_app(app)
    app.register_blueprint(main)

    return app

