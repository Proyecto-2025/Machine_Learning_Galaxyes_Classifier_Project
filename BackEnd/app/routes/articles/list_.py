from flask import jsonify
from .. import api_bp
from ...models.article_model import Article

@api_bp.route("/articles", methods=["GET"])
def list_articles():
    articles = Article.query.order_by(Article.id.asc()).all()
    data = [{"id": a.id, "titulo": a.titulo, "resumen": a.resumen} for a in articles]
    return jsonify(data), 200
