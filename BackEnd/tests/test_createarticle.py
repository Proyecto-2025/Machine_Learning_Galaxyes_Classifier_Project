from unittest.mock import MagicMock
from app.routes.articles import create as create_articles_module



def _mock_db_and_article_to_dict(monkeypatch):
    """
    Devuelve (fake_session, fake_article_to_dict) y deja patcheado:
    - create_articles_module.db.session
    - create_articles_module.article_to_dict
    """

    fake_session = MagicMock()
    fake_db = MagicMock()
    fake_db.session = fake_session

    monkeypatch.setattr(create_articles_module, "db", fake_db, raising=False)

    def fake_article_to_dict(article):
 
        return {
            "id": getattr(article, "id", 1),
            "titulo": article.titulo,
            "resumen": article.resumen,
            "cuerpoArticulo": article.cuerpo_articulo,
            "creation_date": "2025-01-01T00:00:00",
            "foto": getattr(article, "foto", None),
        }

    monkeypatch.setattr(
        create_articles_module,
        "article_to_dict",
        fake_article_to_dict,
        raising=False,
    )

    return fake_session, fake_article_to_dict


def test_create_single_article_success(client, monkeypatch):
    fake_session, _ = _mock_db_and_article_to_dict(monkeypatch)

    payload = {
        "titulo": "Nuevo artículo",
        "resumen": "Un resumen",
        "cuerpo_articulo": "Contenido del artículo",
    }

    response = client.post("/api/v1/articles", json=payload)

    assert response.status_code == 201
    data = response.get_json()

    assert data["titulo"] == "Nuevo artículo"
    assert data["resumen"] == "Un resumen"
    assert data["cuerpoArticulo"] == "Contenido del artículo"


    fake_session.add.assert_called_once()
    fake_session.commit.assert_called_once()


def test_create_single_article_with_camel_case_body(client, monkeypatch):
    fake_session, _ = _mock_db_and_article_to_dict(monkeypatch)

    payload = {
        "titulo": "Artículo camel",
        "resumen": "Resumen camel",
        "cuerpoArticulo": "Contenido camelCase",
    }

    response = client.post("/api/v1/articles", json=payload)

    assert response.status_code == 201
    data = response.get_json()

    assert data["titulo"] == "Artículo camel"
    assert data["resumen"] == "Resumen camel"
    assert data["cuerpoArticulo"] == "Contenido camelCase"

    fake_session.add.assert_called_once()
    fake_session.commit.assert_called_once()


def test_create_multiple_articles_success(client, monkeypatch):
    fake_session, _ = _mock_db_and_article_to_dict(monkeypatch)

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


    assert fake_session.add.call_count == 2
    fake_session.commit.assert_called_once()


def test_create_articles_invalid_json(client, monkeypatch):
    fake_session, _ = _mock_db_and_article_to_dict(monkeypatch)

    response = client.post("/api/v1/articles")

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "JSON inválido o ausente"

    fake_session.add.assert_not_called()
    fake_session.commit.assert_not_called()


def test_create_articles_non_dict_element_in_list(client, monkeypatch):
    fake_session, _ = _mock_db_and_article_to_dict(monkeypatch)

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

    fake_session.add.assert_not_called()
    fake_session.commit.assert_not_called()


def test_create_article_missing_title(client, monkeypatch):
    fake_session, _ = _mock_db_and_article_to_dict(monkeypatch)

    payload = {
        "resumen": "Resumen sin título",
        "cuerpo_articulo": "Contenido",
    }

    response = client.post("/api/v1/articles", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert "sin 'titulo' válido" in data["error"]

    fake_session.add.assert_not_called()
    fake_session.commit.assert_not_called()