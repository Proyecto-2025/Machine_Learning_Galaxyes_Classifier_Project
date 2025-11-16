
from flask import jsonify
from datetime import datetime
import random
from . import api_bp
from ..db import db
from ..models.image_model import ImageModel
from ..dependence import get_db_service, get_storage_service

@api_bp.route("/play", methods=["GET"])
def play():
    try:
        
        db_service = get_db_service()
        storage_service = get_storage_service()
        
        ids = db_service.get_all_image_ids()  # add a for loop with owners?
        if not ids:
            return jsonify({"error": "No hay imágenes en la base de datos"}), 404

        random.seed(int(datetime.utcnow().timestamp()))
        random_id = random.choice(ids)
        
        random_image = db_service.search_image_by_id(random_id)
        if not random_image:
            return jsonify({"error": f"Imagen id={random_id} no encontrada"}), 404

        public_url = f"{storage_service.public_base_url}/{random_image.filename}"
        
        return jsonify({
            "filename": public_url,
            "features": random_image.features
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
