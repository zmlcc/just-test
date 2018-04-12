
import os
import click
from myapp import create_app
from myapp.model import db, Group



app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Init the db')
    db.create_all()
    if len(Group.query.filter_by(name="nogroup").all()) == 0:
        nogroup = Group("nogroup")
        db.session.add(nogroup)
        db.session.commit()
        click.echo('Init Table Group')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
    