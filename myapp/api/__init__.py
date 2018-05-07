from flask import Blueprint

from flask_sqlalchemy import get_debug_queries

api = Blueprint('api', __name__)

from .user import *
from .cluster import *
from .project import *


# @api.after_request
# def show_sql(response):
#     for query in get_debug_queries():
#         print(query)
#         print()
#         print()

#     return response