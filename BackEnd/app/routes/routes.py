from flask import jsonify, request
from . import api_bp
from services.response_service import response_service
from services.validation_service import validate_image
from services.com_service import process

@api_bp.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "no image provided"}), 400
    image = request.files["image"]
    
    #Add MIME type check, extension check and/or image verification by processing
    valid, message = validate_image(image)
    if not valid:
        return jsonify({"error": message}), 400
    else
        image128 = image.resize((128,128))

    category = process(image128)

    text = response_service(category)

   """ #Simulated call to ML engine
    result = {
        "label": "galaxy A",
        "confidence": 0.95
    }
    """
    return jsonify({category:text}), 200

#----Server response Test---- 
@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200
