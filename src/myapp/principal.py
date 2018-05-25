from flask import request
from flask import current_app
from flask import g
from flask_principal import Principal, Identity, RoleNeed, Permission
from .model import User

prin = Principal(use_sessions=False)


# mananger_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))


@prin.identity_loader
def load_identity_from_header():
    user_name = request.headers.get("Remote-User", None)
    if user_name is None:
        g.cur_user = None
        current_app.logger.info('username {} g.cur_user {}'.format(user_name, g.cur_user))    
        return None
    
    current_user = User.query.filter_by(name=user_name).first()
    g.cur_user = current_user
    if current_user is None:
        current_app.logger.info('username {} g.cur_user {}'.format(user_name, g.cur_user))    
        return None

    
    identity = Identity(user_name)
    if hasattr(current_user, 'role'):
        for role in current_user.role:
            identity.provides.add(RoleNeed(role.name))

    current_app.logger.info('username {} g.cur_user {}'.format(user_name, g.cur_user))    
    
    return identity