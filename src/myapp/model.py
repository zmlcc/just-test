from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import deferred

db = SQLAlchemy()

prj_user = db.Table(
    "project_user",
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


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def gmt_create(cls): # pylint: disable=e0213
        return db.deferred(
            db.Column(db.DateTime, server_default=db.func.now()))

    @declared_attr
    def gmt_modified(cls):   # pylint: disable=e0213
        return db.deferred(
            db.Column(
                db.DateTime,
                server_default=db.func.now(),
                server_onupdate=db.func.now()))


class Cluster(Base):
    __tablename__ = "cluster"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    addr = db.Column(db.String(80))
    cert = deferred(db.Column(db.Text(2048)))
    access_token = deferred(db.Column(db.Text(2048)))

    def __repr__(self):
        return self.name


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    role = db.relationship(
        "Role",
        secondary=user_role,
        lazy="select",
        backref=db.backref('user', lazy='select'))

    def __repr__(self):
        return self.name


class Role(Base):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Project(Base):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    user = db.relationship(
        "User",
        secondary=prj_user,
        lazy='select',
        backref=db.backref('project', lazy='select'))

    def __repr__(self):
        return self.name


ns_acc = db.Table(
    "namespace_account",
    db.Column(
        "namespace_id", db.Integer, db.ForeignKey("namespace.id"), primary_key=True),
    db.Column(
        "account_id",
        db.Integer,
        db.ForeignKey("account.id"),
        primary_key=True),
)

class Account(Base):
    id = db.Column(db.Integer, primary_key=True)


    token = deferred(db.Column(db.Text(2048)))

    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    cluster = db.relationship("Cluster")
    user = db.relationship("User")

    namespace = db.relationship("Namespace", secondary=ns_acc, lazy="select")

    __table_args__ = (
        db.Index('account_idx', 'cluster_id', 'user_id', unique=True),
    )

    def __repr__(self):
        return "{}@{}".format(self.user.name, self.cluster.name)


class Namespace(Base):
    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(
        db.Integer, db.ForeignKey('cluster.id'),  nullable=False)
    project_id = db.Column(
        db.Integer, db.ForeignKey('project.id'),  nullable=False)

    cluster = db.relationship("Cluster")
    project = db.relationship("Project")

    account = db.relationship("Account", secondary=ns_acc, lazy="select")

    __table_args__ = (
        db.Index('namespace_idx', 'cluster_id', 'project_id', unique=True),
    )


    def __repr__(self):
        return "{}:{}".format(self.cluster.name, self.project.name)
