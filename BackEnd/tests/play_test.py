
def test_no_image_db(client):
    print("Testing play route with an empty database...")
    
    client.application.db_service.get_all_image_ids.return_value = []
    
    response = client.get("/api/v1/play")
    
    assert response.status_code == 404
    json_response = response.get_json()
    assert "No hay imágenes en la base de datos" in json_response.values()
    
def test_image_not_found_db(client):
    print("Testing image not found on database in play route...")
    
    client.application.db_service.get_all_image_ids.return_value = [1]
    client.application.db_service.search_image_by_id.return_value = None
    
    response = client.get("/api/v1/play")
    
    assert response.status_code == 404
    json_response = response.get_json()
    assert "no encontrada" in json_response["error"]
    
def test_succesfull_image_search(client):
    print("Testing succesfull search in play route...")
    client.application.db_service.get_all_image_ids.return_value = [1]
    
    fake_image = type("FakeImage", (), {})()
    fake_image.filename = "test_image.jpeg"
    fake_image.features = {"color": "blue", "size": "large"}
    
    client.application.db_service.search_image_by_id.return_value = fake_image
    client.application.storage_service.public_base_url = "https://fake.url.com"
    
    response = client.get("/api/v1/play")
    json_response = response.get_json()
    
    assert json_response["filename"] == "https://fake.url.com/test_image.jpeg"
    assert json_response["features"] == {"color": "blue", "size": "large"}
    