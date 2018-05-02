from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from ..model import db, User, Project, Cluster, Role, Token, Namespace


admin = Admin()


class BaseModelView(ModelView):
    column_display_all_relations = True
    can_view_details = True
    column_exclude_list = ['gmt_create', 'gmt_modified' ]
    form_excluded_columns = ['gmt_create', 'gmt_modified' ]


class ClusterView(BaseModelView):
    column_list = ('name', 'addr')

class UserView(BaseModelView):
    column_list = ('name', 'role', 'project')
    form_columns = ('name', 'role', 'project')
    # column_editable_list = ('role', 'project')

class ProjectView(BaseModelView):
    column_list = ('name', 'user')
    form_columns = ('name', 'user')

admin.add_view(ClusterView(Cluster, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(BaseModelView(Role, db.session))
admin.add_view(ProjectView(Project, db.session))
admin.add_view(BaseModelView(Token, db.session))
admin.add_view(BaseModelView(Namespace, db.session))

