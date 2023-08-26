import pytest
from fastapi.testclient import TestClient
from WHW14.main import app

client = TestClient(app)

@pytest.fixture
def mock_db_session(monkeypatch):
    monkeypatch.setattr("WHW14.src.routes.contacts.db.get_db", lambda: None)

def test_create_contact(mock_db_session):
    response = client.post("/api/contacts/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    })
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["email"] == "john@example.com"

# Додайте аналогічно інші тести для інших функцій

if __name__ == "__main__":
    pytest.main()
