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
        prediction = ml_json.get("prediction", [])              
        features = ml_json.get("features", [])
        hubble_sequence = ml_json.get("HubbleSequence", [])
        

        #Rewind para guardar con tu storage actual 
        try:
            image_file.stream.seek(0)
            image_bytes = image_file.stream.read()
            image_path = self.storage_service.save(image_bytes)
        except Exception:

            raise

        # Guardar predicción completa en DB 
        self.db_service.save_prediction(image_path,prediction, features, hubble_sequence)
        
        # Devolver tal cual al caller
        return features