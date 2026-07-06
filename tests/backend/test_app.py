import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


def test_signup_for_activity_adds_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@example.com"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_duplicate_signup_returns_error(client):
    activity_name = "Chess Club"
    email = "existing@example.com"
    activities[activity_name]["participants"].append(email)

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown/signup?email=test@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_removes_email_from_activity(client):
    activity_name = "Chess Club"
    email = "student@example.com"
    activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
