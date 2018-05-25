from flask import g
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from ..model import db, User, Project, Cluster, Role, Account, Namespace

from ..principal import admin_permission, load_identity_from_header

admin = Admin()


def can_access_admin():
    identity = load_identity_from_header()
    if identity is None:
        return False
    return identity.can(admin_permission)

class BaseModelView(ModelView):
    column_display_all_relations = True
    can_view_details = True
    # can_delete = False
    action_disallowed_list = ['delete']
    column_exclude_list = ['gmt_create', 'gmt_modified' ]
    form_excluded_columns = ['gmt_create', 'gmt_modified' ]

    def is_accessible(self):
        return True
        if not hasattr(g, "can_access_admin"):
            g.can_access_admin = can_access_admin()
        return g.can_access_admin


class ClusterView(BaseModelView):
    column_list = ('name', 'addr')
    form_columns = ('name', 'addr', 'cert', 'access_token')

class UserView(BaseModelView):
    column_list = ('name', 'role', 'project')
    form_columns = ('name', 'role', 'project')
    # column_editable_list = ('role', 'project')

class ProjectView(BaseModelView):
    column_list = ('name', 'user')
    form_columns = ('name', 'user')

class AccountView(BaseModelView):
    column_list = ('user', 'cluster', 'namespace')
    column_filters = ('user.name',)


admin.add_view(ClusterView(Cluster, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(BaseModelView(Role, db.session))
admin.add_view(ProjectView(Project, db.session))
admin.add_view(AccountView(Account, db.session))
admin.add_view(BaseModelView(Namespace, db.session))

