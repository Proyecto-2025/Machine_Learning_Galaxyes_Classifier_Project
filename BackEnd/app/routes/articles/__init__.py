
from .. import api_bp
from ...models.article_model import Article

def article_to_dict(article: Article):
    return {
        "id": article.id,
        "titulo": article.titulo,
        "resumen": article.resumen,
        "foto": article.foto,
        "cuerpoArticulo": article.cuerpo_articulo,
        "creation_date": article.creation_date.isoformat() if getattr(article, "creation_date", None) else None,
    }
