from app.db import db
from app.models.article_model import Article


def _clear_articles(app):
    """Helper para dejar la tabla articles limpia."""
    with app.app_context():
        Article.query.delete()
        db.session.commit()


def test_create_single_article_success(client):
    app = client.application
    _clear_articles(app)

    payload = {
        "titulo": "Nuevo artículo",
        "resumen": "Un resumen",
        "cuerpo_articulo": "Contenido del artículo"
    }

    response = client.post("/api/v1/articles", json=payload)

    assert response.status_code == 201
    data = response.get_json()

    assert data["titulo"] == "Nuevo artículo"
    assert data["resumen"] == "Un resumen"

    assert data["cuerpoArticulo"] == "Contenido del artículo"


    with app.app_context():
        articles_in_db = Article.query.all()
        assert len(articles_in_db) == 1
        assert articles_in_db[0].titulo == "Nuevo artículo"


def test_create_single_article_with_camel_case_body(client):
    app = client.application
    _clear_articles(app)

    payload = {
        "titulo": "Artículo camel",
        "resumen": "Resumen camel",
        "cuerpoArticulo": "Contenido camelCase"
    }

    response = client.post("/api/v1/articles", json=payload)

    assert response.status_code == 201
    data = response.get_json()

    assert data["titulo"] == "Artículo camel"
    assert data["resumen"] == "Resumen camel"
    assert data["cuerpoArticulo"] == "Contenido camelCase"


def test_create_multiple_articles_success(client):
    app = client.application
    _clear_articles(app)

    payload = [
        {
            "titulo": "Artículo 1",
            "resumen": "Resumen 1",
            "cuerpo_articulo": "Contenido 1",
        },
        {
            "titulo": "Artículo 2",
            "resumen": "Resumen 2",
            "cuerpoArticulo": "Contenido 2",
        },
    ]

    response = client.post("/api/v1/articles", json=payload)

    assert response.status_code == 201
    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["titulo"] == "Artículo 1"
    assert data[0]["resumen"] == "Resumen 1"
    assert data[0]["cuerpoArticulo"] == "Contenido 1"

    assert data[1]["titulo"] == "Artículo 2"
    assert data[1]["resumen"] == "Resumen 2"
    assert data[1]["cuerpoArticulo"] == "Contenido 2"

    with app.app_context():
        assert Article.query.count() == 2


def test_create_articles_invalid_json(client):
    response = client.post("/api/v1/articles")

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "JSON inválido o ausente"


def test_create_articles_non_dict_element_in_list(client):
    payload = [
        "no soy un objeto",
        {
            "titulo": "Artículo válido",
            "resumen": "Resumen",
            "cuerpo_articulo": "Contenido",
        },
    ]

    response = client.post("/api/v1/articles", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert "Elemento #1 no es un objeto JSON válido" in data["error"]


def test_create_article_missing_title(client):
    payload = {
        "resumen": "Resumen sin título",
        "cuerpo_articulo": "Contenido",
    }

    response = client.post("/api/v1/articles", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert "sin 'titulo' válido" in data["error"]
