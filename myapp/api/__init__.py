from flask import Blueprint

from flask_sqlalchemy import get_debug_queries

api = Blueprint('api', __name__)


from . import user
from . import cluster
from . import project
from . import account
from . import premit


# @api.after_request
# def show_sql(response):
#     for query in get_debug_queries():
#         print(query)
#         print()
#         print()

#     return response