from flask import Blueprint

#prefijo comun para las rutas de la API
api_bp = Blueprint ("api", __name__, url_prefix="/api/v1")