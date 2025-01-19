import pytest
from fastapi.testclient import TestClient
from src.api.routes import app

client = TestClient(app)

def test_create_transaction():
    response = client.post(
        "/api/v1/transactions/",
        json={
            "from_address": "addr1",
            "to_address": "addr2",
            "amount": 100
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "pending"

def test_get_transaction():
    # First create a transaction
    create_response = client.post(
        "/api/v1/transactions/",
        json={
            "from_address": "addr1",
            "to_address": "addr2",
            "amount": 100
        }
    )
    tx_id = create_response.json()["id"]
    
    # Then retrieve it
    response = client.get(f"/api/v1/transactions/{tx_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tx_id

def test_get_status():
    response = client.get("/api/v1/status/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data