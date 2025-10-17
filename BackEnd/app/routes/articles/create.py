from flask import jsonify, request
from .. import api_bp
from ...db import db
from ...models.article_model import Article
from . import article_to_dict

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
