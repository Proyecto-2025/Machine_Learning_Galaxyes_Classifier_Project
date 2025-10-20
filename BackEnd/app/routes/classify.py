
from flask import jsonify, request
from . import api_bp
from ..services.validation_service import validate_image
from .dependence import com_service

@api_bp.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "no image provided"}), 400

    image = request.files["image"]

    valid, message = validate_image(image)
    if not valid:
        return jsonify({"error": message}), 400

    try:
        result = com_service.process(image)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
