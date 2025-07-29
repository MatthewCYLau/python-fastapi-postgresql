from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_get_current_user_unauthorized():
    response = client.get("/api/v1/auth")
    assert response.status_code == 401
