from flask import jsonify, request
from . import api_bp
from ..services.validation_service import validate_image
from ..services.com_service import ComService
from ..services.db_service import DbService
from ..services.file_storage_service import FileStorageService


@api_bp.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "no image provided"}), 400
    image = request.files["image"]
    
    #Add MIME type check, extension check and/or image verification by processing
    valid, message = validate_image(image)
    if not valid:
        return jsonify({"error": message}), 400

    db_service = DbService()
    file_storage_service = FileStorageService()
    com_service = ComService(db_service=db_service, storage_service= file_storage_service)
    
    result = com_service.process(image)
    
     
    return jsonify({
        "filename": result["similar_image_filename"],
        "features": result["features"]
        }), 200


