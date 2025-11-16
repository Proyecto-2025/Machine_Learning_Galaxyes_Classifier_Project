from unittest.mock import MagicMock
from app.models.article_model import Article


def test_list_articles_returns_articles(client, monkeypatch):
    app = client.application


    a1 = MagicMock()
    a1.id = 1
    a1.titulo = "Artículo 1"
    a1.resumen = "Resumen 1"

    a2 = MagicMock()
    a2.id = 2
    a2.titulo = "Artículo 2"
    a2.resumen = "Resumen 2"

    fake_list = [a1, a2]


    fake_query = MagicMock()
    fake_query.order_by.return_value = fake_query
    fake_query.all.return_value = fake_list

    with app.app_context():
        monkeypatch.setattr(Article, "query", fake_query, raising=False)

    response = client.get("/api/v1/articles")
    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2

    assert data[0]["id"] == 1
    assert data[0]["titulo"] == "Artículo 1"
    assert data[0]["resumen"] == "Resumen 1"

    assert data[1]["id"] == 2
    assert data[1]["titulo"] == "Artículo 2"
    assert data[1]["resumen"] == "Resumen 2"


def test_list_articles_empty(client, monkeypatch):
    app = client.application

    fake_query = MagicMock()
    fake_query.order_by.return_value = fake_query
    fake_query.all.return_value = []

    with app.app_context():
        monkeypatch.setattr(Article, "query", fake_query, raising=False)

    response = client.get("/api/v1/articles")
    assert response.status_code == 200
    assert response.get_json() == []
