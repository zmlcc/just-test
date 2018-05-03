from flask import request
from flask import current_app
from flask_principal import Principal, Identity, RoleNeed, AnonymousIdentity, Permission
from .model import db, User

prin = Principal()

create_user_permission = Permission(RoleNeed('create_user'))


@prin.identity_loader
def load_identity_from_header():
    user_name = request.headers.get("Remote-User", None)
    current_app.logger.info('get username {}'.format(user_name))
    if user_name is None:
        return None
    
    current_user = User.query.filter_by(name=user_name).first()
    if current_user is None:
        current_app.logger.info('add db username {}'.format(user_name))
        user = User()
        user.name = user_name
        db.session().add(user)
        db.session().commit()
    else:
        current_app.logger.info("get current_user {}".format(current_user))
    
    identity = Identity(user_name)
    if hasattr(current_user, 'role'):
        for role in current_user.role:
            identity.provides.add(RoleNeed(role.name))
    return identity