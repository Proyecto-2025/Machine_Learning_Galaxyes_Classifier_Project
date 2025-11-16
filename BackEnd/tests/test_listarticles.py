from app.db import db
from app.models.article_model import Article


def test_list_articles_returns_articles(client):
  app = client.application
  with app.app_context():

    Article.query.delete()
    db.session.commit()

    a1 = Article(
        titulo="Artículo 1",
        resumen="Resumen 1",
        cuerpo_articulo="Contenido del artículo 1"
    )
    
    a2 = Article(
        titulo="Artículo 2",
        resumen="Resumen 2",
        cuerpo_articulo="Contenido del artículo 2"
    )

    db.session.add_all([a1, a2])
    db.session.commit()
    id1, id2 = a1.id, a2.id 

  response = client.get("/api/v1/articles")
  assert response.status_code == 200

  json_response = response.get_json()

  assert len(json_response) == 2
  assert json_response[0]["id"] == id1
  assert json_response[0]["titulo"] == "Artículo 1"
  assert json_response[0]["resumen"] == "Resumen 1"
  
  assert json_response[1]["id"] == id2
  assert json_response[1]["titulo"] == "Artículo 2"
  assert json_response[1]["resumen"] == "Resumen 2"


def test_list_articles_empty(client):
  app = client.application

  with app.app_context():
    Article.query.delete()
    db.session.commit()

  response = client.get("/api/v1/articles")
  assert response.status_code == 200
  assert response.get_json() == []
