from flask import Blueprint, request, jsonify
from model.PredictGalaxy import makePrediction
from model.Response import Response


controller_bp = Blueprint("controller", __name__)

@controller_bp.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files["image"]
    
    try:
        raw_prediction = makePrediction(image_file)    # Array de probabilidades
        response_obj = Response(raw_prediction)        # Lo paso por Response
        prediction = [round(float(p), 3) for p in response_obj.prediction] # Predicciones redondeadas
        features = response_obj.features               # Las features mas importantes
        hubble_sequence = response_obj.hubble_sequence
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    return jsonify({
        "prediction": prediction,
        "features": features,
        "hubblesequence": hubble_sequence
    }), 200

