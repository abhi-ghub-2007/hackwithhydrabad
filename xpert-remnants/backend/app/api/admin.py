from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db, engine
from app.models.models import (
    Organization, Expert, Project, Technology, DecisionMemory,
    Decision, Incident, Meeting, KnowledgeRisk, Feedback
)
from app.schemas.schemas import AdminStatusResponse, SeedRequest, SeedResponse
from app.services.hindsight_service import hindsight_service
from app.services.llm_service import llm_service
from app.services.batch_processor import batch_processor
from app.scripts.seed_database import seed_database
from app.core.config import settings

router = APIRouter()

@router.get("/admin/status", response_model=AdminStatusResponse)
def get_system_status(db: Session = Depends(get_db)):
    """
    Returns system diagnostic status across PostgreSQL, Hindsight, and LLM (Section 38 & 59).
    """
    db_connected = True
    try:
        db.execute(DecisionMemory.__table__.select().limit(1))
    except Exception:
        db_connected = False

    counts = {
        "memories": db.query(DecisionMemory).count(),
        "verified_memories": db.query(DecisionMemory).filter(DecisionMemory.status == "ACTIVE").count(),
        "needs_review": db.query(DecisionMemory).filter(DecisionMemory.status.in_(["DRAFT", "REVIEW_REQUIRED"])).count(),
        "decisions": db.query(Decision).count(),
        "incidents": db.query(Incident).count(),
        "experts": db.query(Expert).count(),
        "projects": db.query(Project).count(),
        "technologies": db.query(Technology).count(),
        "knowledge_risks": db.query(KnowledgeRisk).count(),
        "feedbacks": db.query(Feedback).count(),
    }

    return AdminStatusResponse(
        database={
            "type": "PostgreSQL" if "postgresql" in str(engine.url) else "SQLite (Local Fallback)",
            "connected": db_connected,
            "url_masked": str(engine.url).split("@")[-1] if "@" in str(engine.url) else str(engine.url)
        },
        hindsight={
            "bank_id": settings.HINDSIGHT_BANK_ID,
            "base_url": settings.HINDSIGHT_BASE_URL,
            "mode": "Cloud Live SDK" if hindsight_service.is_live() else "Local Fallback Memory Engine",
            "connected": True,
            "is_configured": settings.is_hindsight_configured
        },
        llm={
            "provider": settings.LLM_PROVIDER,
            "model": settings.LLM_MODEL,
            "is_configured": settings.is_llm_configured,
            "mode": "Live Provider API" if settings.is_llm_configured else "Local Synthesis Engine"
        },
        counts=counts,
        system_version=settings.VERSION
    )

@router.post("/admin/seed", response_model=SeedResponse)
def trigger_seed(request: SeedRequest):
    """
    Triggers synthetic data generation with profile (DEV, DEMO, FULL, STRESS) (Section 21).
    """
    res = seed_database(profile_name=request.profile, force=True)
    db = next(get_db())
    counts = {
        "memories": db.query(DecisionMemory).count(),
        "decisions": db.query(Decision).count(),
        "incidents": db.query(Incident).count(),
        "experts": db.query(Expert).count(),
        "projects": db.query(Project).count()
    }
    return SeedResponse(
        status="success",
        profile=request.profile,
        seeded_counts=counts
    )

@router.post("/admin/sync-hindsight")
def sync_memories_to_hindsight(db: Session = Depends(get_db)):
    """
    Batch retains all active database memories into the Hindsight memory bank (Section 25).
    """
    memories = db.query(DecisionMemory).filter(DecisionMemory.status == "ACTIVE").all()
    mem_dicts = [
        {
            "id": m.id,
            "problem": m.problem,
            "context": m.context,
            "decision": m.decision,
            "reasoning": m.reasoning,
            "action_taken": m.action_taken,
            "impact": m.impact,
            "lessons_learned": m.lessons_learned,
            "project_id": m.project_id,
            "expert_id": m.expert_id,
            "memory_type": m.memory_type,
            "status": m.status
        }
        for m in memories
    ]
    res = batch_processor.process_memories(mem_dicts, bank_id=settings.HINDSIGHT_BANK_ID)
    return res
