from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_memories():
    response = client.get("/api/memories?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "problem" in data[0]
    assert "decision" in data[0]

def test_filter_memories():
    response = client.get("/api/memories?type=decision&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for mem in data:
        assert mem["memory_type"] == "decision"

def test_create_memory():
    payload = {
        "problem": "Redis cluster evicted customer auth tokens under load.",
        "context": "Customer Identity service during flash sale.",
        "options_considered": "Increase RAM vs partition session keys.",
        "decision": "Partitioned session keys and configured volatile-lru.",
        "reasoning": "Telemetry showed non-expiring keys filled memory.",
        "action_taken": "Updated redis config and deployed cache separation.",
        "impact": "Eliminated token evictions completely.",
        "lessons_learned": "Never mix permanent cache with ephemeral sessions.",
        "memory_type": "decision",
        "status": "ACTIVE",
        "organization_id": 1
    }
    response = client.post("/api/memories", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["problem"] == payload["problem"]
    assert data["hindsight_memory_id"] is not None
    assert data["verification_status"] == "VERIFIED"

def test_document_extraction_and_human_approval():
    """
    Tests Section 23 & 37:
    AI extraction starts as DRAFT.
    Human approval moves it to ACTIVE and retains to Hindsight.
    """
    extract_payload = {
        "title": "Postmortem: Payment Gateway TLS Certificate Expiry",
        "content": "On Oct 12, Payment API experienced 502 errors when upstream mTLS cert expired. Lead engineer switched to automated cert-manager renewal with 30-day pre-expiry alerts.",
        "project_id": 1,
        "file_type": "TXT"
    }
    response = client.post("/api/memories/extract", json=extract_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "REVIEW_PENDING"
    assert len(data["extracted_memories"]) > 0

    draft_mem = data["extracted_memories"][0]
    assert draft_mem["status"] == "DRAFT"
    assert draft_mem["verification_status"] == "UNVERIFIED"

    # Human Approval
    mem_id = draft_mem["id"]
    approve_res = client.put(f"/api/memories/{mem_id}/approve")
    assert approve_res.status_code == 200
    approved_data = approve_res.json()
    assert approved_data["status"] == "ACTIVE"
    assert approved_data["verification_status"] == "VERIFIED"
    assert approved_data["hindsight_memory_id"] is not None
