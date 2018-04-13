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
    project = db.relationship("Project", secondary=prj_user, lazy='subquery', 
    backref=db.backref('user', lazy='subquery'))

    def __init__(self, name="NO_USER_NAME"):
        self.name = name

    def __repr__(self):
        return 'u-{}'.format(self.name)
        

class Project(db.Model):
    __tablename__='project'    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name="NO_PROJECT_NAME"):
        self.name = name

    def __repr__(self):
        return 'prj-{}'.format(self.name)


