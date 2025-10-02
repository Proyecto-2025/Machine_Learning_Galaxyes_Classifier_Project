from flask import jsonify, request
from . import api_bp
from ..services.validation_service import validate_image
from ..services.com_service import ComService
from ..services.db_service import DbService
from ..services.file_storage_service import FileStorageService
import random
from datetime import datetime
from ..models.image_model import ImageModel
from ..db import db

db_service = DbService()
file_storage_service = FileStorageService()
com_service = ComService(db_service=db_service, storage_service= file_storage_service)

@api_bp.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "no image provided"}), 400
    image = request.files["image"]
    
    #Add MIME type check, extension check and/or image verification by processing
    valid, message = validate_image(image)
    if not valid:
        return jsonify({"error": message}), 400
    
    #Process the image a returns a list of features
    try:    
        result = com_service.process(image)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route ("/play", methods = ["POST"])
def play():
    try:
        #Creates a list with all the ids from the database
        ids = [i[0] for i in db.session.query(ImageModel.id).all()]
    
        #sets a seed based on the actual time
        seed = int(datetime.utcnow().timestamp())
    
        #use the seed to generate a random number
        random.seed(seed)
    
        #search for a random register in the database
        random_id = random.choice(ids)
    
        random_image = db_service.search_image_by_id(random_id)
    
        random_image_filename = random_image.filename
    
        random_image_features = random_image.features
    
        return jsonify ({
            "filename": random_image_filename,
            "features": random_image_features
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
