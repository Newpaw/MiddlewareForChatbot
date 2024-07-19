from app.webhooks import router
from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


client = TestClient(router)


def test_receive_non_text_webhook():
    response = client.post("/", json={"activity": "Ping"})
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_receive_webhook():
    response = client.post("/", json={"activity": "Text", "text": "Hello, World!", "sessionId": 123,
                           "timestamp": datetime.now().isoformat(), "language": "en", "source": "user"})
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
