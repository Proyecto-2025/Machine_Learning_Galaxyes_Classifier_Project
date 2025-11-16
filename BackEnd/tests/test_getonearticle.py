from unittest.mock import MagicMock
from app.models.article_model import Article
from app.routes.articles import get_one as get_one_module


def test_get_article_success(client, monkeypatch):
    app = client.application


    fake_article = MagicMock()
    fake_article.id = 1
    fake_article.titulo = "Artículo Test"
    fake_article.resumen = "Resumen Test"
    fake_article.cuerpo_articulo = "Contenido Test"


    fake_query = MagicMock()
    fake_query.get.return_value = fake_article

    with app.app_context():
        monkeypatch.setattr(Article, "query", fake_query, raising=False)


    def fake_article_to_dict(article):
        assert article is fake_article
        return {
            "id": 1,
            "titulo": "Artículo Test",
            "resumen": "Resumen Test",
            "cuerpoArticulo": "Contenido Test",
            "creation_date": "2025-01-01T00:00:00",
            "foto": None,
        }

    monkeypatch.setattr(
        get_one_module, "article_to_dict", fake_article_to_dict, raising=False
    )

    response = client.get("/api/v1/articles/1")
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == 1
    assert data["titulo"] == "Artículo Test"
    assert data["resumen"] == "Resumen Test"
    assert data["cuerpoArticulo"] == "Contenido Test"


def test_get_article_not_found(client, monkeypatch):
    app = client.application

    fake_query = MagicMock()
    fake_query.get.return_value = None  # siempre no encontrado

    with app.app_context():
        monkeypatch.setattr(Article, "query", fake_query, raising=False)

    response = client.get("/api/v1/articles/99999")
    assert response.status_code == 404

    data = response.get_json()
    assert data["error"] == "Artículo no encontrado"