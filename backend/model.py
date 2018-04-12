from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __init__(self, username):
        self.name = username


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    user = db.relationship('User', backref='group', lazy='dynamic')

    def __init__(self, name):
        self.name = name


