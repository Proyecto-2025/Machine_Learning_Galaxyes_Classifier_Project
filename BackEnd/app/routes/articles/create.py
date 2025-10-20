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
            resumen = item.get("resumen")
            foto = item.get("foto")

            cuerpo = item.get("cuerpo_articulo")
            if cuerpo is None:
                cuerpo = item.get("cuerpoArticulo")

            if not titulo or not isinstance(titulo, str) or not titulo.strip():
                return jsonify({"error": f"Elemento #{idx} sin 'titulo' válido"}), 400
            if not resumen or not isinstance(resumen, str) or not resumen.strip():
                return jsonify({"error": f"Elemento #{idx} sin 'resumen' válido"}), 400
            if not cuerpo or not isinstance(cuerpo, str) or not cuerpo.strip():
                return jsonify({"error": f"Elemento #{idx} sin 'cuerpo_articulo' válido"}), 400

            article = Article(
                titulo=titulo.strip(),
                resumen=resumen.strip(),
                foto=foto.strip() if isinstance(foto, str) else foto,
                cuerpo_articulo=cuerpo.strip(),
            )
            db.session.add(article)
            created.append(article)

        db.session.commit()

        if isinstance(data, list):
            return jsonify([article_to_dict(a) for a in created]), 201
        else:
            return jsonify(article_to_dict(created[0])), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudieron crear los artículos", "detail": str(e)}), 500
