import json
import logging

import pytest
from fastapi.testclient import TestClient

from app.main import app

AUTH = {"Authorization": "Bearer demo-alex"}
ALLOWED_LOG_FIELDS = {"request_id", "path", "status", "ms", "error"}


@pytest.fixture
def client():
    return TestClient(app)


def test_rejects_missing_or_wrong_token(client):
    for headers in [{}, {"Authorization": "Bearer wrong-token"}]:
        response = client.get("/v1/me/next-steps", headers=headers)
        assert response.status_code == 401
        assert response.json() == {"error": "unauthorized"}


def test_keeps_health_data_private(client, caplog):
    with caplog.at_level(logging.INFO, logger="next_steps"):
        response = client.get("/v1/me/next-steps", headers=AUTH)
    assert response.headers["Cache-Control"] == "no-store"
    assert response.json()["member"] == {"preferred_name": "Alex"}
    for record in caplog.records:
        assert set(json.loads(record.getMessage())) <= ALLOWED_LOG_FIELDS
