from app.models.image_model import ImageModel
from app.db import db
from datetime import datetime

class DbService:
    
   @staticmethod
   def save_prediction(filename: str, category: str):
       
       img = ImageModel(
           filename = filename,
           category = category,
           creation_date = datetime.now()
       ) 
       
       db.session.add(img)
       db.session.commit()
       return img
    
    