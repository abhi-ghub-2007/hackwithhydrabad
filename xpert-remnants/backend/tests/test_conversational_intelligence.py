"""
Tests for Conversational Intelligence, Open-Knowledge Fallback,
and Decision Memory Evolution (Antigravity 3.8 Flash).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.database import SessionLocal
from app.models.models import DecisionMemory, MemoryRelationship, Project

client = TestClient(app)

def test_greeting_routing():
    """
    Problem A: Greetings must respond directly without triggering Hindsight.
    """
    for q in ["Hello", "Hi", "Good morning", "Hey"]:
        resp = client.post("/api/ask", json={"query": q})
        assert resp.status_code == 200
        data = resp.json()
        assert data["historical_match_score"] == "Direct"
        assert "Hello! I am XPERT REMNANTS" in data["answer"]
        assert len(data["sources"]) == 0
        assert len(data["relevant_experiences"]) == 0

def test_small_talk_routing():
    """
    Problem A: Small talk / acknowledgments must respond directly without Hindsight retrieval.
    """
    for q in ["Thanks", "Thank you", "Okay", "Cool", "Got it"]:
        resp = client.post("/api/ask", json={"query": q})
        assert resp.status_code == 200
        data = resp.json()
        assert data["historical_match_score"] == "Direct"
        assert len(data["sources"]) == 0

def test_identity_and_capabilities_routing():
    """
    Problem A: Identity & Capability questions must answer from system configuration.
    """
    resp_id = client.post("/api/ask", json={"query": "Who are you?"})
    assert resp_id.status_code == 200
    data_id = resp_id.json()
    assert data_id["historical_match_score"] == "Meta"
    assert "SYS-CONFIG" in data_id["sources"]
    assert "XPERT REMNANTS" in data_id["answer"]

    resp_cap = client.post("/api/ask", json={"query": "What can you do?"})
    assert resp_cap.status_code == 200
    data_cap = resp_cap.json()
    assert data_cap["historical_match_score"] == "Meta"
    assert "SYS-CONFIG" in data_cap["sources"]
    assert "Recall Past Decisions" in data_cap["answer"]

def test_open_general_knowledge_fallback():
    """
    Problem B: What is PostgreSQL?
    Must answer using public/general knowledge, clearly separating Org Memory from Public Knowledge.
    Must NOT fabricate an expert decision.
    """
    resp = client.post("/api/ask", json={"query": "What is PostgreSQL?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["historical_match_score"] == "OpenKnowledge"
    assert "PUBLIC-KNOWLEDGE" in data["sources"]
    assert "### Organizational Memory" in data["answer"]
    assert "No preserved expert decision specifically covers" in data["answer"]
    assert "### General / Public Knowledge" in data["answer"]
    assert len(data["relevant_experiences"]) == 0

def test_expert_specific_no_hallucination():
    """
    Section 7 & 25: Never invent expert opinions when unrecorded.
    """
    resp = client.post("/api/ask", json={"query": "What did Raj decide about quantum cryptography algorithm selection?"})
    assert resp.status_code == 200
    data = resp.json()
    # Must refuse safely without pretending Raj had an opinion
    assert data["historical_match_score"] == "Low"
    assert "couldn't find enough preserved expert evidence" in data["answer"].lower() or "no preserved" in data["answer"].lower()
    assert len(data["relevant_experiences"]) == 0

def test_mandatory_decision_evolution_scenario():
    """
    Section 31: Mandatory End-to-End Scenario:
    Step 1: User asks "Which database should we use for Project X?"
            Returns historical records showing Supabase was previously rejected.
    Step 3: User says "No. For the current project we're choosing Supabase because it gives us faster delivery and the team already has experience with it."
    Step 4: System asks "Should I record this as the current active project decision?"
    Step 5: User confirms ("Yes, please record it").
    Step 6: System commits decision, preserves old record, creates supersedes relationship.
    Step 7: User asks "Which database should we use for Project X?"
            System explains current decision (Supabase) + historical context (previously rejected under earlier constraints).
    """
    session_id = f"test_session_scenario_{int(pytest.__version__.replace('.', ''))}"
    db = SessionLocal()
    try:
        # Step 1: User asks about database for Project X
        resp1 = client.post("/api/ask", json={
            "query": "Which database should we use for Project X?",
            "conversation_id": session_id
        })
        assert resp1.status_code == 200
        data1 = resp1.json()
        assert "Supabase" in data1["answer"] or "PostgreSQL" in data1["answer"]
        assert len(data1["sources"]) > 0

        # Step 3: User proposes decision change with rationale
        change_query = (
            "No. For the current project we're choosing Supabase because it gives us "
            "faster delivery and the team already has experience with it."
        )
        resp2 = client.post("/api/ask", json={
            "query": change_query,
            "conversation_id": session_id
        })
        assert resp2.status_code == 200
        data2 = resp2.json()
        # Step 4: System asks confirmation
        assert "Should I record this as the current active project decision?" in data2["answer"]

        # Step 5: User confirms
        resp3 = client.post("/api/ask", json={
            "query": "Yes, please record it.",
            "conversation_id": session_id
        })
        assert resp3.status_code == 200
        data3 = resp3.json()
        assert data3["historical_match_score"] == "High"
        assert "recorded and synchronized to organizational memory" in data3["answer"]
        assert "Supabase selected (Active)" in data3["answer"]
        assert "Supersedes previous decision" in data3["answer"]
        assert len(data3["sources"]) >= 2

        # Step 6: Verify database state: both old and new exist, supersedes relationship exists
        new_mem_id = data3["decision_memory_id"]
        assert new_mem_id is not None
        new_mem = db.query(DecisionMemory).filter(DecisionMemory.id == new_mem_id).first()
        assert new_mem is not None
        assert new_mem.is_current is True
        assert new_mem.decision_status == "ACTIVE"
        assert new_mem.supersedes_memory_id is not None

        # Verify old memory is preserved (never deleted!)
        old_mem = db.query(DecisionMemory).filter(DecisionMemory.id == new_mem.supersedes_memory_id).first()
        assert old_mem is not None
        assert old_mem.is_current is False
        assert old_mem.decision_status == "SUPERSEDED"
        assert "rejected" in old_mem.decision.lower()

        # Verify MemoryRelationship
        rel = db.query(MemoryRelationship).filter(
            MemoryRelationship.source_memory_id == new_mem.id,
            MemoryRelationship.target_memory_id == old_mem.id
        ).first()
        assert rel is not None
        assert rel.relationship_type == "supersedes"

        # Step 7: Future query asking "Which database should we use for Project X?"
        resp4 = client.post("/api/ask", json={
            "query": "Which database should we use for Project X?",
            "conversation_id": session_id
        })
        assert resp4.status_code == 200
        data4 = resp4.json()
        ans4 = data4["answer"]
        # Must explain current choice (Supabase) + historical context (previously rejected) + reason for current choice
        assert "current recorded decision for Project X is Supabase" in ans4
        assert "previously rejected" in ans4
        assert "faster delivery" in ans4
        assert len(data4["sources"]) >= 2
    finally:
        db.close()

def test_missing_reason_capturing_flow():
    """
    Section 11: If user says "Use Supabase instead", system asks for the reason
    before committing the decision.
    """
    session_id = "test_missing_reason_session"
    resp1 = client.post("/api/ask", json={
        "query": "Use Supabase instead.",
        "conversation_id": session_id
    })
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert "What is the main reason for changing the previous decision" in data1["answer"]

    # Provide the reason in turn 2
    resp2 = client.post("/api/ask", json={
        "query": "Because the team already has extensive expertise and needs rapid delivery.",
        "conversation_id": session_id
    })
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert "Should I record this as the current active project decision?" in data2["answer"]

def test_are_you_mad_conversational():
    """
    Contract Requirement: "Are you mad?" must answer directly:
    "No. I don’t have emotions, but I can still help." without Hindsight retrieval.
    """
    resp = client.post("/api/ask", json={"query": "Are you mad?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["historical_match_score"] == "Direct"
    assert "No. I don’t have emotions, but I can still help" in data["answer"]
    assert len(data["sources"]) == 0

def test_simple_fact_database_and_product():
    """
    Contract Requirement: "What database is used?" returns the direct factual answer
    without a dump of unrelated pool sizing or incident postmortems.
    """
    resp = client.post("/api/ask", json={"query": "What database is used?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] in ["SIMPLE_FACT", "PROJECT_QUERY"]
    assert "PostgreSQL" in data["answer"] or "Supabase" in data["answer"]
    assert "billing ledger project" in data["answer"] or "Project X" in data["answer"]
    assert len(data["sources"]) > 0

    # Direct product assignment query
    resp_prod = client.post("/api/ask", json={"query": "Tell me which product you worked on?"})
    assert resp_prod.status_code == 200
    data_prod = resp_prod.json()
    assert "Visual Studio Code" in data_prod["answer"] or "project" in data_prod["answer"].lower()
    assert len(data_prod["sources"]) > 0

def test_multi_turn_follow_ups():
    """
    Contract Requirement: Multi-turn follow-ups:
    Turn 1: "Which database should we use for Project X?"
    Turn 2: "Why?" -> preserves previous turn's database topic and explains why.
    Turn 3: "What about Supabase?" -> evaluates Supabase in context.
    """
    session_id = "test_multi_turn_follow_up_session"
    resp1 = client.post("/api/ask", json={
        "query": "Which database should we use for Project X?",
        "conversation_id": session_id
    })
    assert resp1.status_code == 200

    # Turn 2: "Why?"
    resp2 = client.post("/api/ask", json={
        "query": "Why?",
        "conversation_id": session_id
    })
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["intent"] == "FOLLOW_UP"
    assert "compliance" in data2["answer"].lower() or "latency" in data2["answer"].lower()
    assert len(data2["sources"]) > 0

    # Turn 3: "What about Supabase?"
    resp3 = client.post("/api/ask", json={
        "query": "What about Supabase?",
        "conversation_id": session_id
    })
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["intent"] == "FOLLOW_UP"
    assert "Supabase" in data3["answer"]
    assert len(data3["sources"]) > 0

def test_topic_drift_isolation():
    """
    Contract Requirement: Unrelated questions do not inherit old conversation context.
    After talking about databases, asking about Kafka should resolve against Kafka.
    """
    session_id = "test_topic_drift_session"
    # Turn 1: Database question
    client.post("/api/ask", json={
        "query": "What database is used?",
        "conversation_id": session_id
    })

    # Turn 2: Distinct Kafka query
    resp2 = client.post("/api/ask", json={
        "query": "What architectural pattern was applied for Kafka event streaming?",
        "conversation_id": session_id
    })
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["intent"] in ["DOMAIN_QUERY", "PROJECT_QUERY"]
    assert len(data2["sources"]) > 0
    # Must not force database answer into Kafka query
    assert "Kafka" in data2["answer"] or "event" in data2["answer"].lower()

def test_feedback_loop_outcome_capture():
    """
    Contract Requirement: POST /api/ask/feedback creates new empirical evidence,
    updates decision memory, and syncs to Hindsight.
    """
    fb_payload = {
        "ask_query": "How should database connection pool be configured under high concurrency?",
        "feedback_type": "HELPFUL",
        "actual_result": "Applied transaction pooling with PgBouncer; context switching thrashing reduced by 85%.",
        "decision_memory_id": 100001
    }
    resp = client.post("/api/ask/feedback", json=fb_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "recorded successfully" in data["message"]

