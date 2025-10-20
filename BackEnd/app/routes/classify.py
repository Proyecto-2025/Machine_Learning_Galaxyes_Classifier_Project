
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

    # 1️⃣ Validar imagen
    valid, message = validate_image(image)
    if not valid:
        return jsonify({"error": message}), 400

    # 2️⃣ Leer bytes de la imagen una sola vez
    image_bytes = image.read()
    image.seek(0)  # reset para que se pueda guardar

    try:
        # 3️⃣ Llamar al ML Engine
        result = com_service.process(io.BytesIO(image_bytes))

        # 4️⃣ Extraer predicción
        prediction = result.get("prediction")
        features = result.get("features")
        hubble_sequence = result.get("hubblesequence")

        # 5️⃣ Guardar imagen en almacenamiento local
        filename = storage_service.save(io.BytesIO(image_bytes))

        # 6️⃣ Guardar predicción en la DB
        db_service.save_prediction(filename, prediction, features, hubble_sequence)

        # 7️⃣ Devolver resultado al cliente
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
