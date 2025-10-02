from datetime import datetime
from ..db import db
import json

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False) #Almacena la Url de la imagen
    prediction = db.Column(db.JSON, nullable=False)
    features = db.Column(db.JSON, nullable=False) # Lista de features
    hubble_sequence = db.Column(db.JSON, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow) #¿Es necesario fijar la hora de Argentina?
    