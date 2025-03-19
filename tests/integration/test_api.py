from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Chatbot API"}

def test_chat_endpoint():
    response = client.post(
        "/chat/chat",
        json={"message": "What is Python?"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert "sources" in response.json()

def test_nlp_analyze_endpoint():
    response = client.post(
        "/nlp/analyze",
        json={"text": "Test message for analysis"}
    )
    assert response.status_code == 200
    assert "status" in response.json()
    assert "analysis" in response.json()