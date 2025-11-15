import io
from PIL import Image
import requests

class ComService:       
    def process(self, image_bytes_io):
        """
        Recibe un io.BytesIO con la imagen
        """
        ml_engine_url = "https://mlengine-production.up.railway.app/predict"

        try:
            img = Image.open(image_bytes_io)
            img_bytes_io = io.BytesIO()
            img.save(img_bytes_io, format=img.format or "JPEG")
            img_bytes_io.seek(0)

            files = {"image": ("uploaded_image.jpg", img_bytes_io, "image/jpeg")}
            response = requests.post(ml_engine_url, files=files, timeout=1000)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.ConnectionError:
            return {"error": "Unable to connect to ML Engine"}
        except requests.exceptions.Timeout:
            return {"error": "Exceeded wait time while connecting to ML Engine"}
        except requests.exceptions.RequestException as e:
            return {"error": f"HTTP Error: {str(e)}"}
        except ValueError:
            return {"error": "Invalid JSON response from ML Engine"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}


