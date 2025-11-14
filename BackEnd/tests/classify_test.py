import io
from PIL import Image


#----------------------- Route/classify test ------------------------------#

def test_no_image(client):
    print("Testing no image response on route classify...")
    
    response = client.post("/api/v1/classify")   
   
    assert response.status_code == 400, f"Status code should be 400, but instead is: {response.status_code}"
    json_response = response.get_json()
    assert "error" in json_response, "Missing 'error' field in response."
    print("No image test run succesfully!")

def test_invalid_file_extension(client):
    print("Testing invalid file extension response on route classify...")
    
    file = { "image": (io.BytesIO(b"this is not a real image"), "not_an_image.txt", "text/plain")}
    
    response = client.post("/api/v1/classify", data=file, content_type="multipart/form-data")
    
    assert response.status_code == 400, f"Status code should be 400, but instead is: {response.status_code}"
    json_response = response.get_json()
    assert "Formato no permitido. Solo JPG y PNG" in json_response.values()
    print("Invalid file extension test run succesfully!")
    
def test_invalid_file_MIME(client):
    print("Testing invalid file MIME type response on route classify...")
    
    file = { "image": (io.BytesIO(b"this is not a real image"), "not_an_image.jpg", "text/plain")}
    
    response = client.post("/api/v1/classify", data=file, content_type="multipart/form-data")
    
    assert response.status_code == 400, f"Status code should be 400, but instead is: {response.status_code}"
    json_response = response.get_json()
    assert "El tipo de archivo no es valido" in json_response.values()
    print( "Invalid MIME type test run succesfully!")
    
def test_invalid_file_size(client):
    print("Testing invalid file size response on route classify...")
    
    big_image = b"a" * (6 * 1024 * 1024)
    
    
    file = { "image": (io.BytesIO(big_image), "very_big.jpg", "image/jpeg")}
    
    response = client.post("/api/v1/classify", data=file, content_type="multipart/form-data")
    
    assert response.status_code == 400, f"Status code should be 400, but instead is: {response.status_code}"
    json_response = response.get_json()
    assert "El archivo supera los 5MB" in json_response.values()
    print("Invalid file size test run succesfully!")
    
def test_invalid_image(client):
    print("Testing invalid image response on route classify...")
    
    file = { "image": (io.BytesIO(b""), "imvalid_image.jpg", "image/jpeg")}
    
    response = client.post("/api/v1/classify", data=file, content_type="multipart/form-data")
    
    assert response.status_code == 400, f"Status code should be 400, but instead is: {response.status_code}"
    json_response = response.get_json()
    assert "El archivo no es una imagen válida." in json_response.values()
    print("Invalid image test run succesfully!")
    
def test_valid_classify(client):
    print("Testing valid call to classify route...")
    
    def create_test_image(format = "JPEG", size = (100, 100), color= (255, 0, 0)):
        img = Image.new("RGB", size, color)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format = format)
        img_bytes.seek(0)
        return img_bytes
    
    com = client.application.com_service
    storage = client.application.storage_service
    db = client.application.db_service
    
    com.process.return_value = {
                "prediction": "spiral",
                "features": {"f1": 0.0},
                "hubblesequence": "Sb"
    }
            
    db.save_prediction.return_value = None
        
    storage.save.return_value = "fake_url"
    
    image = create_test_image()
    file = {"image": (image, "fake_image.jpg", "image/jpeg")}
    
    response = client.post("api/v1/classify", data= file, content_type="multipart/form-data")
    
    assert response.status_code == 200
    
    print("Valid call test to classify route run succesfully!")
    
def test_invalid_classify(client):
    print("Testing invalid call to ML response...")
    
    def create_test_image(format = "JPEG", size = (100, 100), color= (255, 0, 0)):
        img = Image.new("RGB", size, color)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format = format)
        img_bytes.seek(0)
        return img_bytes    
    
    com = client.application.com_service
    storage = client.application.storage_service
    db = client.application.db_service
    
    com.process.side_effect = Exception("Unable to connect to ML Engine")
            
    db.save_prediction.return_value = None
        
    storage.save.return_value = "fake_url"
    
    image = create_test_image()
    file = {"image": (image, "fake_image.jpg", "image/jpeg")}
    
    response = client.post("api/v1/classify", data=file, content_type= "multipart/form-data")
    
    assert response.status_code == 500
    json_response = response.get_json()
    assert "Unable to connect to ML Engine" in json_response.values()
    print("Invalid call to ML test run succesfully!")

def test_invalid_ml_response(client):
    print("Testing invalid response from ML...")
    
    def create_test_image(format = "JPEG", size = (100, 100), color= (255, 0, 0)):
        img = Image.new("RGB", size, color)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format = format)
        img_bytes.seek(0)
        return img_bytes    
    
    com = client.application.com_service
    storage = client.application.storage_service
    db = client.application.db_service
    
    com.process.return_value = {"prediction": "spiral"}
            
    db.save_prediction.return_value = None
    
    image = create_test_image()    
    storage.save.return_value = "fake_url"
            
    file = {"image": (image, "fake_image.jpg", "image/jpeg")}
    
    response = client.post("api/v1/classify", data= file, content_type="multipart/form-data")
    
    assert response.status_code == 500
    json_response = response.get_json()
    assert  "Null or invalid response from the ML" in json_response.values()

    print("Invalid response from ML test run succesfully!")

