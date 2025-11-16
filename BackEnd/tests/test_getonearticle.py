from app.db import db
from app.models.article_model import Article


def test_get_article_success(client):
    app = client.application

    with app.app_context():
        Article.query.delete()
        db.session.commit()

        article = Article(
            titulo="Artículo Test",
            resumen="Resumen Test",
            cuerpo_articulo="Contenido Test"
        )
        db.session.add(article)
        db.session.commit()

        article_id = article.id


    response = client.get(f"/api/v1/articles/{article_id}")
    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == article_id
    assert data["titulo"] == "Artículo Test"
    assert data["resumen"] == "Resumen Test"
    assert "cuerpoArticulo" in data
    assert data["cuerpoArticulo"] == "Contenido Test"



def test_get_article_not_found(client):

    response = client.get("/api/v1/articles/99999")
    assert response.status_code == 404

    data = response.get_json()
    assert data["error"] == "Artículo no encontrado"