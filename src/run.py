
import os
import click
from myapp import create_app
from myapp.model import db, User, Role



app = create_app(os.getenv('FLASK_CONFIG') or 'default')




@app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Init the db')
    db.create_all()
    


@app.cli.command()
@click.option('--name', prompt='sso name',
              help='The person to greet.')
def add_admin(name):
    if 0 == len(name) :
        return

    role = Role.query.filter_by(name="admin").first()
    if role is None:
        role = Role()
        role.name = "admin"
        db.session.add(role)
        db.session.commit()

    user = User.query.filter_by(name=name).first()
    if user is None:
        user = User()
        user.name = name
        db.session.add(user)

    user.role.append(role)
    db.session.commit()

    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
    