import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


def test_unregister_participant_removes_email_from_activity(client):
    activity_name = "Chess Club"
    email = "student@example.com"
    activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
