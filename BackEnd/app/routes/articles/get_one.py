from flask import jsonify
from .. import api_bp
from ...models.article_model import Article
from . import article_to_dict

@api_bp.route("/articles/<int:article_id>", methods=["GET"])
def get_article(article_id):
    article = Article.query.get(article_id)
    if not article:
        return jsonify({"error": f"Artículo con id={article_id} no encontrado"}), 404
    return jsonify(article_to_dict(article)), 200
