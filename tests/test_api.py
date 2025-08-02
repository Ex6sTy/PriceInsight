from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_predict():
    response = client.post(
        "/predict/",
        json={"count": 500, "add_cost": 3000, "mean_competitor_price": 60000},
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert isinstance(data["predicted_price"], float)


def test_predict_invalid():
    # Отправляем невалидные данные
    response = client.post(
        "/predict/",
        json={
            "count": "abc",  # не число!
            "add_cost": 3000,
            "mean_competitor_price": 60000,
        },
    )
    assert response.status_code == 422
