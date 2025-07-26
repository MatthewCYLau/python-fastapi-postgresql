import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


@pytest.fixture()
def mocked_repository(mocker):
    mock_user_data = {
        "id": uuid.uuid4(),
        "email": "hello@example.com",
        "created_at": datetime.now(),
        "password": "testpassword",
    }
    mocker.patch(
        "api.user.repository.UserRepository.get_all",
        return_value=[mock_user_data],
    )
    mocker.patch(
        "api.user.repository.UserRepository.create", return_value=mock_user_data
    )
    mocker.patch(
        "api.user.repository.UserRepository.get_by_id", return_value=mock_user_data
    )


def test_get_users(mocked_repository):
    response = client.get("/api/v1/users")
    assert response.status_code == 200


def test_create_user(mocked_repository):
    response = client.post(
        "/api/v1/users", json={"email": "one@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201


def test_get_user_by_id(mocked_repository):
    response = client.get(f"/api/v1/users/{uuid.uuid4()}")
    assert response.status_code == 200
