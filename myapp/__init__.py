from flask import Flask
from .model import db
from .main import main


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    app.register_blueprint(main)
    return app



