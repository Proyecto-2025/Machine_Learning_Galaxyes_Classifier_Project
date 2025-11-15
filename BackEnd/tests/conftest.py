import pytest
from unittest.mock import MagicMock
from app import create_app

@pytest.fixture
def client():

    # Create mocks
    storage_mock = MagicMock()
    db_mock = MagicMock()
    com_mock = MagicMock()

    # Use mocks to create app
    app = create_app(
        db_service=db_mock,
        storage_service=storage_mock,
        com_service=com_mock
    )

    app.config['TESTING'] = True

    # Flask client
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_mocks(client):

    client.application.com_service.reset_mock()
    client.application.db_service.reset_mock()
    client.application.storage_service.reset_mock()
