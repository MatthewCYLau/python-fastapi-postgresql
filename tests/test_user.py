import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient

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


def test_get_users(mocked_repository):
    response = client.get("/api/v1/users")
    assert response.status_code == 200
