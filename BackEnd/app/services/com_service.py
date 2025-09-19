from file_storage_service import FileStorageService

class ComService:
    def __init__(self, ml_engine, db_service, storage_service):
        
        self.ml_engine = ml_engine
        
        self.db_service = db_service
        
        self.storage_service = storage_service
        
    def process(self, image):

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
            image_path = self.storage_service.save(image_file)
        except Exception:

            raise

        # Guardar predicción completa en DB 

        # Buscar una imagen cualquiera que cumpla esos features

        # Devolver tal cual al caller
        return {
            "prediction": ml_json,
            "saved_image_path": image_path,
        }