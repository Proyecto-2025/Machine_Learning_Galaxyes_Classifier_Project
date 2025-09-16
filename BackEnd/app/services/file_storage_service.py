import os
import uuid
from datetime import datetime
from PIL import Image
import io

class FileStorageService:
    
    def __init__(self, base_dir="uploads"):
        
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True) #Creates main dir if not exists
    
    def save(self, image):
        
        today = datetime.now().strftime("%d-%m-%Y")
        date_dir = os.path.join(self.base_dir, today)
        os.makedirs(date_dir, exist_ok=True)
        
        img = Image.open(io.BytesIO(image))
        ext = f".{img.format.lower()}" #Get extension from image
        
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(date_dir, filename)
        
        img.save(filepath)
        
        return filepath   