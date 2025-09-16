from file_storage_service import FileStorageService

class ComService:
    def __init__(self, ml_engine, db_service, storage_service):
        
        self.ml_engine = ml_engine
        
        self.db_service = db_service
        
        self.storage_service = storage_service
        
    def process(self, image):
        
        #Calls Ml engine and gets a prediction(category)
        category = self.ml_engine.predict(image) 
        
        #Saves the file and gets its path
        image_path = self.storage_service.save(image)
        
        #Saves image (filepath) and prediction in DB
        self.db_service.save_prediction(image_path, category)
        
        #¿Returns prediction for route purpose?
        return category