"""
End-to-End Acceptance Test for XPERT REMNANTS (Antigravity 3.8 Flash)
Covers all requirements from Sections 30, 34, 35, and 61 (Scenarios A through M).
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.models import DecisionMemory, KnowledgeUpdate, LearningEvent, MemoryRelationship, Project

client = TestClient(app)

def test_full_acceptance_trajectory():
    session_id = f"test_full_acceptance_session_{int(pytest.__version__.replace('.', ''))}"
    db = SessionLocal()
    try:
        # A: Discover projects
        resp_a = client.post("/api/ask", json={"query": "Which projects are available?", "conversation_id": session_id})
        assert resp_a.status_code == 200
        data_a = resp_a.json()
        assert "Visual Studio Code" in data_a["answer"]
        assert "Windows Terminal" in data_a["answer"]
        assert "PowerToys" in data_a["answer"]

        # B: Greetings & Identity (Contract: Direct answer, no Hindsight dump)
        resp_hello = client.post("/api/ask", json={"query": "Hello", "conversation_id": session_id})
        assert resp_hello.status_code == 200
        assert "Hello! I am XPERT REMNANTS" in resp_hello.json()["answer"]
        assert len(resp_hello.json()["sources"]) == 0

        resp_ident = client.post("/api/ask", json={"query": "Tell me about yourself", "conversation_id": session_id})
        assert resp_ident.status_code == 200
        assert "organizational expertise memory" in resp_ident.json()["answer"].lower()
        assert "SYS-CONFIG" in resp_ident.json()["sources"]

        resp_cap = client.post("/api/ask", json={"query": "What can you do?", "conversation_id": session_id})
        assert resp_cap.status_code == 200
        assert "recall past decisions" in resp_cap.json()["answer"].lower()
        assert "SYS-CONFIG" in resp_cap.json()["sources"]

        # C: General Technical Knowledge (No unrelated organizational memory dump)
        resp_gen = client.post("/api/ask", json={
            "query": "Which is better, hidden coupling or explicit interfaces?",
            "conversation_id": session_id
        })
        assert resp_gen.status_code == 200
        assert "explicit interfaces" in resp_gen.json()["answer"].lower()

        # D: Expert Discovery & Continuity
        resp_exp_list = client.post("/api/ask", json={"query": "List all experts", "conversation_id": session_id})
        assert resp_exp_list.status_code == 200
        assert "Senior" in resp_exp_list.json()["answer"] or "Architect" in resp_exp_list.json()["answer"]

        resp_active_exp = client.post("/api/ask", json={"query": "Active experts?", "conversation_id": session_id})
        assert resp_active_exp.status_code == 200
        assert "active" in resp_active_exp.json()["answer"].lower()

        resp_names = client.post("/api/ask", json={"query": "Will you name them?", "conversation_id": session_id})
        assert resp_names.status_code == 200
        assert len(resp_names.json()["answer"]) > 10

        # E: Initial Decision Query: What database is used?
        resp_db1 = client.post("/api/ask", json={"query": "Which database is used?", "conversation_id": session_id})
        assert resp_db1.status_code == 200
        data_db1 = resp_db1.json()
        assert "PostgreSQL" in data_db1["answer"] or "Supabase" in data_db1["answer"]

        # F: Follow-up: Why?
        resp_why = client.post("/api/ask", json={"query": "Why?", "conversation_id": session_id})
        assert resp_why.status_code == 200
        data_why = resp_why.json()
        assert "compliance" in data_why["answer"].lower() or "latency" in data_why["answer"].lower()

        # G: Historical Trial: What did they try before?
        resp_tried = client.post("/api/ask", json={"query": "What did they try before?", "conversation_id": session_id})
        assert resp_tried.status_code == 200
        assert "Supabase" in resp_tried.json()["answer"] or "caching" in resp_tried.json()["answer"]

        # H: Historical Failure: Why didn't that approach work?
        resp_failed = client.post("/api/ask", json={"query": "Why didn't that approach work?", "conversation_id": session_id})
        assert resp_failed.status_code == 200
        assert "connection" in resp_failed.json()["answer"].lower() or "latency" in resp_failed.json()["answer"].lower()

        # I: Historical Lessons: What did the previous engineers learn about database scalability?
        resp_lessons = client.post("/api/ask", json={
            "query": "What did the previous engineers learn about database scalability?",
            "conversation_id": session_id
        })
        assert resp_lessons.status_code == 200
        assert "Connection Pooling" in resp_lessons.json()["answer"] or "pool" in resp_lessons.json()["answer"].lower()

        # J: Section 30 Decision Change Multi-turn Flow
        # Turn 1: Propose change with reason
        resp_change1 = client.post("/api/ask", json={
            "query": "I am switching to PostgreSQL because of company preference and standardization.",
            "conversation_id": session_id
        })
        assert resp_change1.status_code == 200
        data_change1 = resp_change1.json()
        # System asks which project
        assert "Which project is this for?" in data_change1["answer"]

        # Turn 2: Provide project
        resp_change2 = client.post("/api/ask", json={
            "query": "Project X. I'm making the change today.",
            "conversation_id": session_id
        })
        assert resp_change2.status_code == 200
        data_change2 = resp_change2.json()
        assert "recorded and synchronized to organizational memory" in data_change2["answer"]
        assert "PostgreSQL selected (Active)" in data_change2["answer"]

        # K: Decision State Verification: Which database are we using now?
        resp_curr = client.post("/api/ask", json={"query": "Which database are we using now?", "conversation_id": session_id})
        assert resp_curr.status_code == 200
        assert "PostgreSQL" in resp_curr.json()["answer"]

        # L: Follow-up Reason: Why did we switch?
        resp_switch_reason = client.post("/api/ask", json={"query": "Why did we switch?", "conversation_id": session_id})
        assert resp_switch_reason.status_code == 200
        assert "company preference" in resp_switch_reason.json()["answer"].lower()

        # M: Continuous Learning & Verified Correction: We discovered the issue was actually connection pooling
        resp_corr = client.post("/api/ask", json={
            "query": "We discovered the issue was actually connection pooling",
            "conversation_id": session_id
        })
        assert resp_corr.status_code == 200
        data_corr = resp_corr.json()
        assert "verified root cause as connection pooling" in data_corr["answer"].lower()
        assert "connection pooling" in data_corr["answer"].lower()

        # Verify KnowledgeUpdate & LearningEvent were persisted in database
        ku = db.query(KnowledgeUpdate).filter(KnowledgeUpdate.new_state.ilike("%connection pooling%")).first()
        assert ku is not None
        assert ku.update_type in ["CORRECTION", "PROJECT_UPDATE"]

        le = db.query(LearningEvent).filter(LearningEvent.content.ilike("%connection pooling%")).first()
        assert le is not None
        assert le.promotion_status == "PERSISTED"

    finally:
        db.close()
