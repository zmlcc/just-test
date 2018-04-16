from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    gmt_create = db.Column(db.DateTime, server_default=db.func.now())
    gmt_modified = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now())


user_prj = db.Table(
    "user_project",
    db.Column(
        "user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "project_id",
        db.Integer,
        db.ForeignKey("project.id"),
        primary_key=True),
)

user_role = db.Table(
    "user_role",
    db.Column(
        "user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    project = db.relationship(
        "Project",
        secondary=user_prj,
        lazy='subquery',
        backref=db.backref('user', lazy='subquery'))

    role = db.relationship(
        "Role",
        secondary=user_role,
        lazy="subquery",
        backref=db.backref('user', lazy='subquery'))

    def __init__(self, name="NO_USER_NAME"):
        self.name = name

    def __repr__(self):
        return self.name


class Project(Base):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name="NO_PROJECT_NAME"):
        self.name = name

    def __repr__(self):
        return self.name


class Cluster(Base):
    __tablename__ = "cluster"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name="NO_CLUSTER_NAME"):
        self.name = name

    def __repr__(self):
        return self.name


class Role(Base):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name="NO_ROLE_NAME"):
        self.name = name

    def __repr__(self):
        return self.name