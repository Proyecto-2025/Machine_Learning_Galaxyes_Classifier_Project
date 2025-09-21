import io
import os
import shutil
from datetime import datetime
from PIL import Image
from pathlib import Path
from app.services.com_service import ComService
from app.services.file_storage_service import FileStorageService

#----------------------- Route/classify test ------------------------------#

def test_route_classify(client, app, db_service, monkeypatch):
   
    #Creates a test upload folder (and clean it if exists)
    upload_dir = Path("uploads_test")
    if upload_dir.exists():
        shutil.rmtree(upload_dir)
    upload_dir.mkdir()
    
    #instance of file_storage-service
    storage_service = FileStorageService(base_dir = upload_dir)
    
    #monkeypatch to replace ComService's process method in order to emulate the ML engine
    def fake_process(self, image_file):
        image_file.seek(0)
        raw_bytes = image_file.read()
        filename = storage_service.save(raw_bytes)
        features = ["SUAVE", "VISTA DE PERFIL"]
        db_service.save_prediction(filename, features)
        return {
            "similar_image_filename": filename, 
            "features": features
        }
    
    monkeypatch.setattr(ComService, "process", fake_process)
    
    #create fake image
    img_bytes = io.BytesIO() 
    img = Image.new("RGB", (100, 100), color= "blue")
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    
    #POST to /classify
    data = {"image": (img_bytes, "test_classify.jpg")}
    response = client.post("/api/v1/classify", data = data, content_type = "multipart/form-data")
    
    #verify response
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["features"] == ["SUAVE", "VISTA DE PERFIL"]
    assert os.path.exists(json_data["filename"])
    
    #today's folder created by FileStorageService
    today_dir = datetime.now().strftime("%d-%m-%Y")
    expected_dir = upload_dir / today_dir
    assert expected_dir.exists()
    
    #verify thath today's folder contains a file
    files = os.listdir(expected_dir)
    assert len(files) == 1
    
    #verify that the file really exists
    saved_path = os.path.join(expected_dir, files[0])
    assert os.path.exists(saved_path)
    
    #verify that DB contains the record
    json_data = response.get_json()
    file_path = json_data["filename"] 
    
    with app.app_context():
        imgs = db_service.free_image_searching(image_url = file_path)
        assert len(imgs) == 1
        assert imgs[0].filename == str(saved_path)