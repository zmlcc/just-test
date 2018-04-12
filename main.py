
import os
from flask import Flask
# from backend import  db
import backend
import click
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)


    return app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Init the db')
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
    