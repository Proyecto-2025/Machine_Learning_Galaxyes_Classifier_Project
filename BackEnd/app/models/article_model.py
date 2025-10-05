
from datetime import datetime
from ..db import db

class Article(db.Model):
    __tablename__ = "articles"  

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    resumen = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(255), nullable=True)  
    cuerpo_articulo = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
