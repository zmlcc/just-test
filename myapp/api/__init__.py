from flask import Blueprint

api = Blueprint('api', __name__)

from .user import *
from .cluster import *
from .project import *