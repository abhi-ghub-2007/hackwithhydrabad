from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_decisions():
    response = client.get("/api/decisions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_decision_replay_timeline():
    """
    Tests Section 39 Decision Replay timeline:
    Problem detected -> Investigation -> Decision -> Action -> Outcome -> Lesson.
    """
    response = client.get("/api/decisions/1")
    assert response.status_code == 200
    data = response.json()
    assert "decision_id" in data
    assert "steps" in data
    assert len(data["steps"]) == 6
    stages = [s["stage"] for s in data["steps"]]
    assert "Problem Detected" in stages
    assert "Investigation & Options Evaluated" in stages
    assert "Decision Formulated" in stages
    assert "Action Executed" in stages
    assert "Realized Outcome" in stages
    assert "Lessons Learned & Warnings" in stages
