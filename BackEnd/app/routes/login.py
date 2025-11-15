from flask import jsonify, request
from . import api_bp
from dependence import get_db_service
from ..services.password_service import PasswordService
import jwt
from datetime import datetime, timedelta

@api_bp.route("/api/v1/login", methods=["POST"])
def login():
  data = request.get_json()

  if not data:
    return jsonify({"error": "Debes enviar un json"}), 400

  email = data.get("email")
  password = data.get("password")

  if not email:
    return jsonify({"error":"Falta email"}), 400

  if not password:
    return jsonify({"error":"Falta password"})

  db_service = get_db_service

  user = db_service.search_user_by_email("email")

  if not user:
    return jsonify({"Error": "Email o contraseña incorrectos"}) , 401

  if not PasswordService.verify_password(password, user.password_hash):
    return jsonify({"error": "Email o contraseña incorrectos"}), 401


  expiracion = datetime.utcnow() + timedelta(hours=2)

  payload = {
      "sub": user.id,
      "email": user.email,
      "exp": expiracion
  }
  token = jwt.encode(
      payload,
      current_app.config["SECRET_KEY"],
      algorithm="HS256"
  )
  return jsonify({
    "success": "Login exitoso",
    "token": token,
    "user": {
        "id": user.id,
        "email": user.email,
        "username": user.username
    }
  }), 200
