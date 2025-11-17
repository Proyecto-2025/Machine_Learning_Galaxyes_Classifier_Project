from ..models.image_model import ImageModel
from ..models.user_model import User
from ..models.user_info_model import UserInfo
from ..db import db
from datetime import datetime
from sqlalchemy import extract
import json

class DbService:
    
   @staticmethod
   def save_prediction(filename: str, prediction: list[float], features: list[str], hubble_sequence: list[str] ):
       
       img = ImageModel(
           filename = filename,
           prediction = prediction,
           features = features,
           hubble_sequence = hubble_sequence,
           creation_date = datetime.now()
       ) 
       db.session.add(img)
       db.session.commit()
   
   #For gaming purpose? 
   def search_image_by_id(self, image_id: int) -> ImageModel | None:
        
       return ImageModel.query.get(image_id)
   
   #search images by a list of features
   def search_image_by_features(self, required_features: list[str]) -> list[ImageModel]:
       
       results = []
       all_images = ImageModel.query.all()
       for image in all_images:
           image_features = image.get_features()
           if all(f in image_features for f in required_features):
               results.append(image)
       return results
   
   #search images by url, day, month or year of register
   def free_image_searching(
       self,
       image_url: str | None = None,
       year: int | None = None,
       month: int | None = None,
       day: int | None = None,
   )-> list[ImageModel]:
       
       query = ImageModel.query
       
       if image_url:
           query = query.filter(ImageModel.filename.like(f"%{image_url}%"))       
            
       if year:
           query = query.filter(extract("year", ImageModel.creation_date) == year) 
           
       if month:
           query = query.filter(extract("month", ImageModel.creation_date) == month)
           
       if day:
           query = query.filter(extract("day", ImageModel.creation_date) == day)   
       
       return query.all()
   
   def search_user_by_email(self, email: str):
        existing_user = User.query.filter_by(email=email).first()
        return existing_user
    
   def get_all_image_ids(self):
        return [row[0] for row in db.session.query(ImageModel.id).all()]
   
   def save_user_and_info(self, email, password_hash, username):
    user = User(
        email=email,
        password_hash=password_hash
    )
    user.info = UserInfo(username=username)
    db.session.add(user)
    db.session.commit()

    
       
   
   
   
   
