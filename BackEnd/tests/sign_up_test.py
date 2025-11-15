from unittest.mock import MagicMock

def test_empty_signUp(client):
    print("Testing empty sign up on signup route...")
    
    response = client.post("/api/v1/signup", json = {})
    
    json_response = response.get_json()
    assert "Los campos usuario, email y password son obligatorios" in json_response.values()
    print("Empty sign up test run succesfully!")
             
def test_no_username(client):
    print("Testing no username sign up on signup route...")
    
    response = client.post("/api/v1/signup", json = {"email": "fake@mail.com", "password": "Password123"})
    
    json_response = response.get_json()
    assert "No se ha ingresado un nombre de usuario" in json_response.values()
    print("No username sign up test run succesfully!")
    
def test_no_password(client):
    print("Testing no password sign up on signup route...")
    
    response = client.post("/api/v1/signup", json = {"username": "name", "email": "fake@mail.com"})
    
    json_response = response.get_json()
    assert "No se ha ingresado una password" in json_response.values()
    print("No password sign up test run succesfully!")
    
def test_no_email(client):
    print("Testing no email sign up on signup route...")
    
    response = client.post("/api/v1/signup", json = {"username": "name", "password": "Password123"})
    
    json_response = response.get_json()
    assert "No se ha ingresado un email" in json_response.values()
    print("No email sign up test run succesfully!")
    
def test_weak_password(client):
    print("Testing weak password sign up on signup route...")
    
    response = client.post("/api/v1/signup", json = {"username": "name", "email": "fake@mail.com", "password": "password"})
    
    json_response = response.get_json()
    assert "La password debe tener al menos 8 caracteres, mayúscula, minúscula y número" in json_response.values()
    print("Weak password sign up test run succesfully!")
    
def test_existing_user(client):
    print("Testing 'email already in use' sign up on ropute signup...")
    
    client.application.db_service.search_user_by_email.return_value = {"id": 1}
    
    response = client.post("/api/v1/signup", json = {"username": "name", "email": "fake@mail.com", "password": "Password123"})
    
    assert response.status_code == 400
    
    json_response = response.get_json()
    assert "Ya existe una cuenta asociada a ese email" in json_response.values()
    print("Email already in use test run succesfully!")
    
def test_succesfull_signUp(client):
    print("Testing succesfull sign up on signup route...")
    
    client.application.db_service.search_user_by_email.return_value = None    
    client.application.db_service.save_user.return_value = None
    
    response = client.post("/api/v1/signup", json = {"username": "name", "email": "fake@mail.com", "password": "Password123"})
    
    assert response.status_code == 201
    
    json_response = response.get_json()
    assert "La cuenta ha sido creada con exito" in json_response.values()