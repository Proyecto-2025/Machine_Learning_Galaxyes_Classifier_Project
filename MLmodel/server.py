from flask import Blueprint, request, jsonify
from model.PredictGalaxy import makePrediction
from model.Response import Response


controller_bp = Blueprint("controller", __name__)

@controller_bp.route("/classify", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files["image"]
    
    try:
        raw_prediction = makePrediction(image_file)   # Array de probabilidades
        response_obj = Response(raw_prediction)       # Lo paso por Response
        features = response_obj.features   # Saco las features mas importantes
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    return jsonify({
        "prediction": features,  # lista de labels activados
    }), 200

