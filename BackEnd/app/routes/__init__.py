from flask import Blueprint

#prefijo comun para las rutas de la API
api_bp = Blueprint ("api", __name__, url_prefix="/api/v1")

from . import classify, play
from .articles import create, list_, get_one