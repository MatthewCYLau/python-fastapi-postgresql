import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
import json

from api.main import app

client = TestClient(app)


@pytest.fixture()
def mocked_repository(mocker):
    mocker.patch(
        "api.user.repository.UserRepository.get_all",
        return_value=[
            {
                "id": uuid.uuid4(),
                "email": "hello@example.com",
                "created_at": datetime.now(),
            }
        ],
    )
    mocker.patch(
        "api.user.repository.UserRepository.create",
        return_value=[
            {
                "id": uuid.uuid4(),
                "email": "hello@example.com",
                "created_at": datetime.now(),
            }
        ],
    )


def test_get_users(mocked_repository):
    response = client.get("/api/v1/users")
    assert response.status_code == 200


def test_create_user(mocked_repository):
    response = client.post("/api/v1/users", json={"email": "one@example.com"})
    assert response.status_code == 201
