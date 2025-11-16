from unittest.mock import MagicMock

def test_login_empty_json(client):

  response = client.post("/api/v1/login", json={})
  json_response = response.get_json()

  assert response.status_code == 400
  assert "Debes enviar un JSON" in json_response.values()



def test_login_no_email(client):

  response = client.post("/api/v1/login", json={
    "password": "Mateo123"
  })

  json_response = response.get_json()

  assert response.status_code == 400
  assert "Ingrese un email por favor" in json_response.values()


def test_login_no_password(client):

  response = client.post("/api/v1/login", json={
    "email": "Mateo@gmail.com"
  })

  json_response = response.get_json()
  assert response.status_code == 400
  assert "Ingrese un password por favor" in json_response.values()



def test_login_user_not_found(client):

    client.application.db_service.search_user_by_email = MagicMock(return_value=None)

    response = client.post("/api/v1/login", json={
        "email": "noexiste@gmail.com",
        "password": "Password123"
    })

    json_response = response.get_json()
    assert response.status_code == 401
    assert "email o contraseña incorrectos" in json_response.values()



def test_login_wrong_password(client):

  fake_user = MagicMock()
  fake_user.password_hash = "hash_incorrecto"
  fake_user.email = "Mateo@gmail.com"
  fake_user.id = 1
  fake_user.username = "Mateo"

  client.application.db_service.search_user_by_email = MagicMock(return_value=fake_user)
  from app.services.password_service import PasswordService

  PasswordService.verify_password = MagicMock(return_value=False)
  response = client.post("/api/v1/login", json={
    "email": "fake@mail.com",
    "password": "Password123" 
  })

  json_response = response.get_json()

  assert response.status_code == 401
  assert "email o contraseña incorrectos" in json_response.values()



def test_login_success(client):
  fake_user = MagicMock()
  fake_user.id = 1
  fake_user.email = "Mateo@gmail.com"
  fake_user.username = "Mateo"
  fake_user.password_hash = "HASH"

  client.application.db_service.search_user_by_email = MagicMock(return_value=fake_user)

  from app.services.password_service import PasswordService
  PasswordService.verify_password = MagicMock(return_value=True)
  import jwt
  jwt.encode = MagicMock(return_value="fake-token")

  response = client.post("/api/v1/login", json={
    "email": "Mateo@gmail.com",
    "password": "Password123"
  })

  json_response = response.get_json()

  assert response.status_code == 200
  assert json_response["token"] == "fake-token"
  assert json_response["user"]["id"] == 1
  assert json_response["user"]["email"] == "Mateo@gmail.com"
