from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


prj_user = db.Table("project_user",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
)
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    project = db.relationship("Project", secondary=prj_user, lazy='dynamic', 
    backref=db.backref('user', lazy='dynamic'))

    def __init__(self, username):
        self.name = username
        

class Project(db.Model):
    __tablename__='project'    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name


