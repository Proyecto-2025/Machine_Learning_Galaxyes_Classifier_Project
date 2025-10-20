from datetime import datetime
from ..db import db
import json

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False) #Almacena la Url de la imagen
    features = db.Column(db.Text, nullable=False) # Lista de features
    creation_date = db.Column(db.DateTime, default=datetime.utcnow) #¿Es necesario fijar la hora de Argentina?
    
    #convert a list of features as json to store it in the DB 
    def set_features(self, features_list):
        self.features = json.dumps(features_list)
        
    #returns a list of features from the stored json
    def get_features(self):
        return json.loads(self.features)
