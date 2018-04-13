from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from ..model import db, User, Project

admin = Admin()

class MyModelViewBase(ModelView):
#    column_display_pk = True # optional, but I like to see the IDs in the list
   column_display_all_relations = True

admin.add_view(MyModelViewBase(User, db.session))
admin.add_view(MyModelViewBase(Project, db.session))

