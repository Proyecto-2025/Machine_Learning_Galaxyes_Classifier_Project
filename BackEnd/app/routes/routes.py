from flask import jsonify, request
from . import api_bp
from ..db import db
from ..services.validation_service import validate_image
from ..services.com_service import ComService
from ..services.db_service import DbService
from ..services.file_storage_service import FileStorageService
from ..models.article_model import Article
from ..models.image_model import ImageModel
from datetime import datetime
import random

db_service = DbService()
file_storage_service = FileStorageService()
com_service = ComService(db_service=db_service, storage_service=file_storage_service)

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


@api_bp.route("/play", methods=["POST"])
def play():
    try:
        # IDs existentes en la DB
        ids = [row[0] for row in db.session.query(ImageModel.id).all()]
        if not ids:
            return jsonify({"error": "No hay imágenes en la base de datos"}), 404

        # Semilla por timestamp actual
        seed = int(datetime.utcnow().timestamp())
        random.seed(seed)

        # ID aleatorio y registro
        random_id = random.choice(ids)
        random_image = db_service.search_image_by_id(random_id)
        if not random_image:
            return jsonify({"error": f"Imagen id={random_id} no encontrada"}), 404

        return jsonify({
            "filename": random_image.filename,
            "features": random_image.features
        }), 200

    except Exception as e:
        # No hay escritura aquí, pero por las dudas si en el futuro se agrega
        try:
            db.session.rollback()
        except Exception:
            pass
        return jsonify({"error": str(e)}), 500


# -------------------- HELPERS ARTÍCULOS --------------------
def article_to_dict(article: Article):
    return {
        "id": article.id,
        "titulo": article.titulo,
        "resumen": article.resumen,
        "foto": article.foto,
        "cuerpoArticulo": article.cuerpo_articulo,
        "creation_date": article.creation_date.isoformat() if getattr(article, "creation_date", None) else None,
    }


# -------------------- ARTÍCULOS: CREATE (uno o varios) --------------------
@api_bp.route("/articles", methods=["POST"])
def create_articles():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "JSON inválido o ausente"}), 400

    payload = data if isinstance(data, list) else [data]
    created = []

    try:
        for idx, item in enumerate(payload, start=1):
            if not isinstance(item, dict):
                return jsonify({"error": f"Elemento #{idx} no es un objeto JSON válido"}), 400

            titulo = item.get("titulo")
            if not titulo or not isinstance(titulo, str):
                return jsonify({"error": f"Elemento #{idx} sin 'titulo' válido"}), 400

            resumen = item.get("resumen")
            foto = item.get("foto")
            cuerpo = item.get("cuerpoArticulo")

            article = Article(
                titulo=titulo.strip(),
                resumen=resumen.strip() if isinstance(resumen, str) else resumen,
                foto=foto.strip() if isinstance(foto, str) else foto,
                cuerpo_articulo=cuerpo if isinstance(cuerpo, str) else cuerpo,
            )
            db.session.add(article)
            created.append(article)

        db.session.commit()
        return jsonify([article_to_dict(a) for a in created]), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudieron crear los artículos", "detail": str(e)}), 500


@api_bp.route("/articles", methods=["GET"])
def list_articles():
    articles = Article.query.order_by(Article.id.asc()).all()
    data = [{"id": a.id, "titulo": a.titulo, "resumen": a.resumen} for a in articles]
    return jsonify(data), 200


@api_bp.route("/articles/<int:article_id>", methods=["GET"])
def get_article(article_id):
    article = Article.query.get(article_id)
    if not article:
        return jsonify({"error": f"Artículo con id={article_id} no encontrado"}), 404
    return jsonify(article_to_dict(article)), 200