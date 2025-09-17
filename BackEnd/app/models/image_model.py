from datetime import datetime
from app.db import db

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False) #Almacena la Url de la imagen
    category = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow) #¿Es necesario fijar la hora de Argentina?
