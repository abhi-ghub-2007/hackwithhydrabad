from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_knowledge_handoff_workflow():
    """
    Tests Section 35: 8-question expert handoff interview.
    """
    payload = {
        "expert_id": 1,
        "project_id": 1,
        "deep_systems": "Payment authorization gateway and database connection pooling cluster.",
        "recurring_problems": "P99 latency spikes during flash sales due to thread pool starvation.",
        "critical_decisions": "Enlarged pool to 100 with acquire timeout of 3000ms (DEC-219).",
        "sop_exceptions": "Standard scale-out SOP fails when DB max_connections limit is approached.",
        "vital_warnings": "Never increase pool beyond 100 without PgBouncer external proxy.",
        "past_failures": "Attempting to scale app pods to 24 crashed DB connection handles.",
        "hidden_dependencies": "Prometheus exporter scrape interval must be aligned with timeout.",
        "successor_lessons": "Always check active connection queue wait times before touching CPU."
    }
    response = client.post("/api/knowledge-handoff", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["created_memories_count"] >= 2
    assert len(data["memories"]) >= 2

def test_knowledge_risks_endpoint():
    """
    Tests Section 36 & 38: Knowledge risks calculation.
    """
    response = client.get("/api/risks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "risk_level" in data[0]
    assert "topic" in data[0]

def test_admin_diagnostics():
    """
    Tests Section 38 & 59 Admin status diagnostics.
    """
    response = client.get("/api/admin/status")
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "hindsight" in data
    assert "llm" in data
    assert "counts" in data
    assert data["counts"]["memories"] > 0
