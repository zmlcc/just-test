from flask_sqlalchemy import SQLAlchemy

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

    gmt_create = db.Column(db.DateTime, server_default=db.func.now())
    gmt_modified = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now())




class Cluster(Base):
    __tablename__ = "cluster"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    cert = db.Column(db.Text(1000))
    addr = db.Column(db.String(80))
    access_token = db.Column(db.Text(1000))

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




class Account(Base):
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(80), unique=True)

    token = db.Column(db.Text(1000))

    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    namespace_id = db.Column(db.Integer, db.ForeignKey('namespace.id'))

    cluster = db.relationship("Cluster")
    user = db.relationship("User")


    def __repr__(self):
        return "{}@{}".format(self.user.name, self.cluster.name) 


class Namespace(Base):
    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), unique=True, nullable=False) 
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), unique=True, nullable=False)

    cluster = db.relationship("Cluster")
    project = db.relationship("Project")
    account = db.relationship("Account")

    def __repr__(self):
        return self.name 


    

