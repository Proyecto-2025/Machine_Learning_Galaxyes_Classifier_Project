
from flask import jsonify, request
from . import api_bp
from ..services.validation_service import validate_image
from .dependence import get_com_service, get_db_service, get_storage_service
import io

@api_bp.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "no image provided"}), 400

    image = request.files["image"]
    com_service = get_com_service()
    db_service = get_db_service()
    storage_service = get_storage_service()

    # Validate image
    valid, message = validate_image(image)
    if not valid:
        return jsonify({"error": message}), 400

    
    image_bytes = image.read()
    image.seek(0)  

    try:
        # Call to ML Engine
        result = com_service.process(io.BytesIO(image_bytes))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    required_keys = {"prediction", "features", "hubblesequence"}
    
    if result and isinstance(result, dict) and required_keys.issubset(result.keys()):
        
         # Extract prediction
        prediction = result.get("prediction")
        features = result.get("features")
        hubble_sequence = result.get("hubblesequence")

        # Save image locally
        filename = storage_service.save(image)

        # Save prediction on DB
        db_service.save_prediction(filename, prediction, features, hubble_sequence)

        # Return to client
        return jsonify(result), 200
    
    else:
        return jsonify({"error": "Null or invalid response from the ML", 
                        "response_recieved": result}), 500
