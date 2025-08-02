import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


@pytest.fixture()
def mocked_repository(mocker):
    mock_product_response = {
        "id": uuid.uuid4(),
        "created_at": datetime.now(),
        "name": "example",
    }
    mock_order_data = {
        "id": uuid.uuid4(),
        "user_id": uuid.uuid4(),
        "product_id": uuid.uuid4(),
        "created_at": datetime.now(),
        "product": mock_product_response,
    }
    mocker.patch(
        "api.order.repository.OrderRepository.get_all",
        return_value=[mock_order_data],
    )


def test_get_orders(mocked_repository):
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
