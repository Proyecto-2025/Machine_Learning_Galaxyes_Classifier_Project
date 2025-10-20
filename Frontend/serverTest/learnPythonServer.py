from flask import Flask,request , jsonify, send_from_directory
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    # 1. Revisar si se envió el archivo
    if "image" not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    file = request.files["image"]

    # 2. Validar nombre de archivo
    if file.filename == "":
        return jsonify({"error": "El archivo no tiene nombre"}), 400

    if file.filename.lower() == "fail.jpg":
            return jsonify({"error": "El archivo fail.jpg no está permitido"}), 400

    # 3. Guardar archivo en carpeta uploads/
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # 4. Respuesta exitosa
    return jsonify({
        "filename": file.filename,
        "features": ["feature1", "feature2", "feature3","feature4", "feature5", "feature6","feature7", "feature8", "feature9"]
    }), 200

@app.route("/articles")
def get_articles():
    articles = [
        {"name": "Black Holes", "resume": "Regions of spacetime where gravity is so strong nothing can escape."},
        {"name": "Dark Matter", "resume": "A mysterious form of matter that makes up most of the universe’s mass."},
        {"name": "Exoplanets", "resume": "Planets that orbit stars outside our solar system."}
    ]
    return jsonify(articles)

@app.route("/randomImage")
def post_ramdom_image():
    return send_from_directory("./","Messier_59.jpg")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
