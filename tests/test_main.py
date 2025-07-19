from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_pint():
    response = client.get("/ping")
    assert response.status_code == 200
