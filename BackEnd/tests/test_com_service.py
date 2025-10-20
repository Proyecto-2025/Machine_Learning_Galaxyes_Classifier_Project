import io
import os
from datetime import datetime
from PIL import Image
from app.services.com_service import ComService

#----------------------- ComService test ------------------------------#

def test_com_service_process(app, db_service, storage_service, monkeypatch):

    
    # ML engine mock to simulate requests
    def fake_process(self, image_file):
        raw_bytes = image_file.read() if hasattr(image_file, "read") else image_file
        filename = storage_service.save(raw_bytes)
        features = ["SUAVE", "VISTA DE PERFIL"]
        db_service.save_prediction(filename, features)
        return filename, features
    
    #monkeypatch to process method to intercept requests
    monkeypatch.setattr(ComService, "process", fake_process)
    
    #create fake image 
    img_bytes = io.BytesIO()
    img = Image.new("RGB", (100,100), color = "blue")
    img.save(img_bytes, format = "JPEG")
    img_bytes.seek(0)
    
    # simulates an user's uploaded file
    class FakeFile:
        def __init__(self, bytes_io, filename):
            self.stream = bytes_io
            self.filename = filename
            self.mimetype = "image/jpeg"
        def read(self):
            self.stream.seek(0)
            return self.stream.read()
        def seek(self, pos):
            self.stream.seek(pos)
        
    fake_file = FakeFile(img_bytes, "test.jpg")
    
    com_service = ComService( db_service, storage_service)
    
    #run process
    with app.app_context():
        filename, features = com_service.process(fake_file)
    
    #verify features
    assert features == ["SUAVE", "VISTA DE PERFIL"]
    
    #present day folder created by FileStorageService
    today_dir = datetime.now().strftime("%d-%m-%Y")
    expected_dir = os.path.join(storage_service.base_dir, today_dir)
    
    #verify that today's folder exist
    assert os.path.exists(expected_dir)
    
    #verify that today's folder contains a file
    files = os.listdir(expected_dir)
    assert len(files) == 1
    
    #verify that the file really exists
    saved_path = os.path.join(expected_dir, files[0])
    assert os.path.exists(saved_path)
    
    #verify that a record exists in DB
    with app.app_context():
        imgs = db_service.free_image_searching(image_url= filename)
        assert len(imgs) == 1
        assert imgs[0].filename == saved_path
    


