from flask import jsonify, request, current_app
from . import api_bp
from ..dependence import get_db_service 
from ..services.password_service import PasswordService
import jwt
from datetime import datetime, timedelta
import os


@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debes enviar un JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email:
        return jsonify({"error": "Ingrese un email por favor"}), 400

    if not password:
        return jsonify({"error": "Ingrese un password por favor"}), 400

    db_service = get_db_service()

    user = db_service.search_user_by_email(email)

    if not user:
        return jsonify({"error": "email o contraseña incorrectos"}), 401

    if not PasswordService.verify_password(password, user.password_hash):
        return jsonify({"error": "email o contraseña incorrectos"}), 401

    expiracion = datetime.utcnow() + timedelta(hours=2)

    payload = {
        "sub": user.id,
        "email": user.email,
        "exp": expiracion
    }

    secret_key = os.environ.get("SECRET_KEY")
    token = jwt.encode(
        payload,
        secret_key,
        algorithm="HS256"
    )

    return jsonify({
        "success": "Login exitoso",
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
        }
    }), 200
