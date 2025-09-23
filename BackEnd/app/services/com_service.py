import requests
from .file_storage_service import FileStorageService


class ComService:
    def __init__(self, db_service, storage_service):
        
        #self.ml_engine = ml_engine
        
        self.db_service = db_service
        
        self.storage_service = storage_service
        
    def process(self, image_file):

        filename = getattr(image_file, "filename", "upload.bin")
        mimetype = getattr(image_file, "mimetype", "application/octet-stream")

        # Leer bytes
        raw = image_file.read()
        if not raw:
            raise ValueError("archivo vacío")

        # POST al microservicio IA 
        files = {"image": (filename, raw, mimetype)}
        try:
            resp = requests.post(f"{self.ml_base_url}/predict", files=files, timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"ml service error: {e}")

        #guardar respuesta prediccion
        ml_json = resp.json()              
        features = ml_json.get("features", [])

        #Rewind para guardar con tu storage actual 
        try:
            image_file.stream.seek(0)
            image_bytes = image_file.stream.read()
            image_path = self.storage_service.save(image_bytes)
        except Exception:

            raise

        # Guardar predicción completa en DB 
        saved_image = self.db_service.save_prediction(image_path, features)

        # Buscar una imagen cualquiera que cumpla esos features
        similar_images = self.db_service.search_by_features(features)
        
        # excluimos la imagen recien cargada
        similar_images = [img for img in similar_images if img.id != saved_image.id]
        
        # guardamos la ruta de la primer imagen que cumpla con las caracteristicas (si existe)
        similar_image_filename = similar_images[0].filename if similar_images else None
        
        # Devolver tal cual al caller
        return {
            "similar_image_filename": similar_image_filename,
            "features": features
        }