import kubernetes.client as k8c


def get_sa_name(username):
    return "u-{}".format(username)


def get_rb_name(role_name, sa_name):
    return "{}~{}".format(role_name, sa_name)


NS_BASE_ROLE = k8c.V1Role(
    api_version="rbac.authorization.k8s.io/v1",
    kind="Role",
    metadata=k8c.V1ObjectMeta(name="r-base"),
    rules=[
        k8c.V1PolicyRule(api_groups=["*"], resources=["*"], verbs=["*"]),
    ],
)


def o2prj(project):
    return dict(name=project.name)



def o2user(user):
    return dict(name=user.name)
