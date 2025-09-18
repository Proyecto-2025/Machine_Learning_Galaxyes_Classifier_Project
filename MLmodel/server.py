from flask import Blueprint, request, jsonify
from model.PredictGalaxy import makePrediction
from model.Response import features_map


controller_bp = Blueprint("controller", __name__)

@controller_bp.route("/classify", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files["image"]
    
    try:
        prediction = makePrediction(image_file)
        # Convertir a string
        pred_strings = [f"{cls}: {prob:.3f}" for cls, prob in zip(features_map, prediction)]
        pred_string = ", ".join(pred_strings)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    return jsonify({"prediction": pred_string}), 200
