from flask import jsonify, request, current_app
from . import api_bp
from ..services.db_service import DbService
from ..services.password_service import PasswordService


@api_bp.route("/signup", methods = ["POST"])

def signup():
    db_service = DbService
    #db_service = current_app.db_service
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Los campos usuario, email y password son obligatorios"}), 400    
    if "username" not in data:
        return jsonify({"error": "No se ha ingresado un nombre de usuario"}), 400
    if "password" not in data:
        return jsonify({"error": "No se ha ingresado una password"}), 400  
    if "email" not in data:
        return jsonify({"error": "No se ha ingresado un email"}), 400
        
    if not PasswordService.strong_pass(data["password"]):
        return jsonify({"error": "La password debe tener al menos 8 caracteres, mayúscula, minúscula y número"}), 400
    
    existing_user = db_service.search_user_by_email(data["email"])

    if existing_user:
        return jsonify({"error": "Ya existe una cuenta asociada a ese email"}), 400
    
    email = data["email"]
    password_hash = PasswordService.hash_password(data["password"])
    username = data["username"]
    db_service.save_user_and_info(email, password_hash, username)
    return jsonify({"success": "La cuenta ha sido creada con exito"}), 201
    
    