# tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Dados Climáticos!"}

def test_read_weather():
    response = client.get("/weather/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_weather_by_city():
    response = client.get("/weather/city/São Paulo")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        first_record = response.json()[0]
        assert "city" in first_record
        assert first_record["city"] == "São Paulo"
