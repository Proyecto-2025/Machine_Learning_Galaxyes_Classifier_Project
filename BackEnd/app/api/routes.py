from flask import jsonify, request
from . import api_bp

@api_bp.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "no image provided"}), 400
    image = request.files["image"]
    
    #Add MIME type check, extension check and/or image verification by processing
    
    #Simulated call to ML engine
    result = {
        "label": "galaxy A",
        "confidence": 0.95
    }
    
    return jsonify(result), 200

#----Server response Test---- 
@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200
    