

def get_sa_name(username):
    return "u-{}".format(username)


def get_rb_name(role_name, sa_name):
    return "{}~{}".format(role_name, sa_name)


def o2prj(project):
    return dict(name=project.name)


def o2role(role):
    return dict(name=role.name)

def o2user(user):
    return dict(name=user.name)
