import pytest
import os
import shutil
from app import create_app
from app.db import db
from app.services.db_service import DbService
from app.services.file_storage_service import FileStorageService

#Flask app fixture
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

#test client fixture        
@pytest.fixture
def client(app):
    return app.test_client()

#DbService fixture
@pytest.fixture
def db_service(app):
    return DbService()

#temp file storage fixture
@pytest.fixture
def tmp_storage():
    path = "tests/tmp_uploads"
    os.makedirs(path, exist_ok=True)
    yield path
    
    #Clean after test
    shutil.rmtree(path)
    
#FileStorageService fixture using temp file storage
@pytest.fixture
def storage_service(tmp_storage):
    return FileStorageService(base_dir=tmp_storage)