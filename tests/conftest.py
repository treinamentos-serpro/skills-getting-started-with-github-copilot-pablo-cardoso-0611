import pytest
from fastapi.testclient import TestClient

from src import app as backend


@pytest.fixture(autouse=True)
def activity_data(monkeypatch):
    data = {
        "Chess Club": {
            "description": "Learn chess strategies",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Art Club": {
            "description": "Explore visual arts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": [],
        },
    }
    monkeypatch.setattr(backend, "activities", data)
    return data


@pytest.fixture
def client(activity_data):
    with TestClient(backend.app) as test_client:
        yield test_client
