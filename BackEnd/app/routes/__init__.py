from flask import Blueprint
from flask_cors import CORS
#prefijo comun para las rutas de la API
api_bp = Blueprint ("api", __name__, url_prefix="/api/v1")

from .classify import * 
from .play import *
from .articles.create import *
from .articles.list_ import * 
from .articles.get_one import *
from .signup import *