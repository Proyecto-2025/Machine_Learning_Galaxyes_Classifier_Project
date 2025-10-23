import os
import uuid
from datetime import datetime
from PIL import Image
import io

class FileStorageService:
    def __init__(self, base_dir="uploads"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def save(self, image):
        """
        image puede ser:
        - FileStorage de Flask
        - io.BytesIO o bytes
        """
        # Convertir FileStorage a bytes si es necesario
        if hasattr(image, "read"):
            image_bytes = image.read()
            image.seek(0)  # opcional
        else:
            # io.BytesIO o bytes
            if isinstance(image, io.BytesIO):
                image_bytes = image.getvalue()
            else:
                image_bytes = image

        today = datetime.now().strftime("%d-%m-%Y")
        date_dir = os.path.join(self.base_dir, today)
        os.makedirs(date_dir, exist_ok=True)

        img = Image.open(io.BytesIO(image_bytes))
        ext = f".{img.format.lower()}"  # Obtener extensión

        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(date_dir, filename)

        img.save(filepath)
        return filepath
