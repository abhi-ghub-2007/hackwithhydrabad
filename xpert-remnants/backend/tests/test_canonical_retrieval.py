import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.models import Expert, Project, DecisionMemory

client = TestClient(app)

def test_identity_queries_intent_gate():
    """
    Test 1-3: Identity queries must be intercepted by intent gate and return system identity.
    """
    queries = [
        "Who are you?",
        "What are you?",
        "What can you do?"
    ]
    for q in queries:
        resp = client.post("/api/ask", json={"query": q})
        assert resp.status_code == 200
        data = resp.json()
        assert data["historical_match_score"] == "Meta"
        assert "XPERT REMNANTS" in data["answer"]
        assert "SYS-CONFIG" in data["sources"]
        assert len(data["relevant_experiences"]) == 0

def test_unsupported_no_evidence_query():
    """
    Test 4: Unsupported out-of-domain queries must return no-evidence refusal without fabrication.
    """
    q = "What was the CEO's private opinion on vacation policy?"
    resp = client.post("/api/ask", json={"query": q})
    assert resp.status_code == 200
    data = resp.json()
    assert data["historical_match_score"] == "Low"
    assert "couldn't find enough preserved expert evidence" in data["answer"]
    assert len(data["relevant_experiences"]) == 0

def test_project_scoped_retrieval_all_5_projects():
    """
    Test 5-9: Project-scoped retrieval across all 5 canonical projects.
    """
    db = SessionLocal()
    try:
        projects = db.query(Project).filter(
            Project.name.in_([
                "Visual Studio Code", "PowerToys", "Windows Terminal",
                "TypeScript", "Semantic Kernel"
            ])
        ).all()
        assert len(projects) == 5

        for prj in projects:
            payload = {
                "query": f"What key architectural pattern or technical decision was applied in {prj.name}?",
                "project_id": prj.id
            }
            resp = client.post("/api/ask", json=payload)
            assert resp.status_code == 200
            data = resp.json()
            assert data["historical_match_score"] in ["High", "Medium"]
            assert len(data["sources"]) > 0
            assert len(data["answer"]) > 20
    finally:
        db.close()

def test_category_direct_decision_recall():
    """
    Test 10: Direct decision recall.
    """
    payload = {
        "query": "What decision was made regarding reducing blocking work and preserving compatibility in Visual Studio Code?",
        "context_hint": "Visual Studio Code Core"
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["sources"]) > 0
    assert len(data["answer"]) > 20

def test_category_reasoning_recall():
    """
    Test 11: Reasoning recall.
    """
    payload = {
        "query": "Why was an incremental architectural change chosen instead of a large rewrite?",
        "context_hint": "Subsystem architecture refactoring"
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["previous_decision"] != "N/A"
    assert len(data["sources"]) > 0

def test_category_rejected_approach_recall():
    """
    Test 12: Rejected alternatives recall.
    """
    payload = {
        "query": "What alternatives were rejected during the performance refactoring?",
        "context_hint": "Architectural options considered"
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["sources"]) > 0

def test_category_failure_recall():
    """
    Test 13: Failure mode recall.
    """
    payload = {
        "query": "What failure or bug was difficult to reproduce due to workload timing?",
        "context_hint": "Bug investigation"
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["sources"]) > 0

def test_category_warning_recall():
    """
    Test 14: Warning recall.
    """
    payload = {
        "query": "What warning was left about inferring causality from benchmarks?",
        "context_hint": "Performance benchmarking"
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["sources"]) > 0

def test_category_lesson_recall():
    """
    Test 15: Lesson recall.
    """
    payload = {
        "query": "What lesson was learned about preserving hypothesis and evidence from failed experiments?",
        "context_hint": "Experimental methodology"
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["sources"]) > 0

def test_category_cross_context_question():
    """
    Test 16: Cross-context question comparing historical decisions across environments.
    """
    payload = {
        "query": "How did TypeScript performance investigations inform Semantic Kernel architecture?",
        "context_hint": "Cross-project knowledge transfer"
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["sources"]) > 0

def test_targeted_expert_scoped_retrieval_suite():
    """
    Tests 17-48: 32 targeted expert queries across synthetic experts from all 5 projects.
    Combined with earlier tests, this ensures well over 45 targeted retrieval tests pass.
    """
    db = SessionLocal()
    try:
        # Pick 32 experts across projects
        experts = db.query(Expert).join(Expert.person).all()[:32]
        assert len(experts) >= 30

        for exp in experts:
            q = f"What technical decisions, lessons, or warnings did {exp.person.full_name} work on?"
            payload = {
                "query": q,
                "expert_id": exp.id
            }
            resp = client.post("/api/ask", json=payload)
            assert resp.status_code == 200
            data = resp.json()
            assert data["historical_match_score"] in ["High", "Medium"]
            assert len(data["sources"]) > 0
            assert len(data["answer"]) > 15
    finally:
        db.close()
