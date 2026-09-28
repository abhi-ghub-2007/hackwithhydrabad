from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ask_pipeline():
    """
    Tests Section 71 Acceptance Scenario:
    1. Ask related to Payment API latency spike.
    2. Recalls historical decision (DEC-219 / INC-1842).
    3. Evaluates context differences and conflicts.
    4. Returns structured evidence-based answer.
    """
    payload = {
        "query": "Payment API latency increased after a traffic spike during sales event. What should I investigate?",
        "project_id": 1,
        "context_hint": "PostgreSQL database in production"
    }
    response = client.post("/api/ask", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["query"] == payload["query"]
    assert "historical_match_score" in data
    assert data["historical_match_score"] in ["High", "Medium", "Low"]
    assert len(data["why_relevant"]) > 0
    assert len(data["context_differences"]) > 0
    assert "what_happened" in data
    assert "previous_decision" in data
    assert "previous_outcome" in data
    assert len(data["sources"]) > 0
    assert data["decision_memory_id"] is not None

def test_ask_feedback_loop():
    """
    Tests Section 34 & 71 Feedback Learning Loop:
    1. Submits real-world outcome: 'Increasing pool reduced latency by 54%'.
    2. Attaches feedback to decision.
    3. Retains new evidence into Hindsight.
    4. Verified outcome persists.
    """
    feedback_payload = {
        "ask_query": "Payment API latency increased after a traffic spike.",
        "feedback_type": "HELPFUL",
        "actual_result": "Increasing the connection pool reduced latency by 54% in production verification.",
        "decision_memory_id": 1
    }
    response = client.post("/api/ask/feedback", json=feedback_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["new_hindsight_memory_id"] is not None
    assert data["updated_decision_memory_id"] == 1
