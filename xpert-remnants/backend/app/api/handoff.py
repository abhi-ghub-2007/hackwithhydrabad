from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import DecisionMemory, Expert, Project
from app.schemas.schemas import KnowledgeHandoffRequest, KnowledgeHandoffResponse, DecisionMemoryResponse
from app.services.hindsight_service import hindsight_service

router = APIRouter()

@router.post("/knowledge-handoff", response_model=KnowledgeHandoffResponse)
def execute_knowledge_handoff(
    handoff: KnowledgeHandoffRequest,
    db: Session = Depends(get_db)
):
    """
    Expert Knowledge Handoff Interview Endpoint (Section 35):
    Ingests the 8 critical architectural handoff dimensions from a departing expert:
    Systems, Recurring Problems, Critical Decisions, SOP Exceptions, Vital Warnings,
    Past Failures, Hidden Dependencies, and Successor Lessons.
    Converts them into verified, persistent DecisionMemory objects and retains them into Hindsight.
    """
    exp = db.query(Expert).filter(Expert.id == handoff.expert_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Expert not found")

    prj = db.query(Project).filter(Project.id == handoff.project_id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")

    memories_to_create = [
        {
            "problem": f"Core Systems Architecture: {handoff.deep_systems}",
            "context": f"Preserved deep systems expertise for {prj.name}",
            "options_considered": "Standard documentation vs comprehensive expert architecture handoff",
            "decision": handoff.critical_decisions,
            "reasoning": f"SOP Realities & Exceptions: {handoff.sop_exceptions}",
            "action_taken": f"Hidden Dependencies Identified: {handoff.hidden_dependencies}",
            "impact": "Eliminated single-expert knowledge risk and established successor baseline.",
            "lessons_learned": f"WARNING: {handoff.vital_warnings} | Advice: {handoff.successor_lessons}",
            "memory_type": "decision",
            "source_type": "EXPERT_HANDOFF"
        },
        {
            "problem": f"Recurring Operational Problems: {handoff.recurring_problems}",
            "context": f"Operational gotchas in {prj.name}",
            "options_considered": f"Past Failures Evaluated: {handoff.past_failures}",
            "decision": "Applied defensive operational controls based on departed architect experience.",
            "reasoning": f"Avoided known pitfalls: {handoff.past_failures}",
            "action_taken": "Encoded into organizational memory bank directives.",
            "impact": "Prevented recurring outages for incoming team.",
            "lessons_learned": handoff.vital_warnings,
            "memory_type": "warning",
            "source_type": "EXPERT_HANDOFF"
        }
    ]

    created_mems = []
    for m in memories_to_create:
        h_content = (
            f"Expert Handoff Knowledge from {exp.role}\n"
            f"Project: {prj.name}\n"
            f"Problem: {m['problem']}\n"
            f"Context: {m['context']}\n"
            f"Decision: {m['decision']}\n"
            f"Reasoning: {m['reasoning']}\n"
            f"Action: {m['action_taken']}\n"
            f"Impact: {m['impact']}\n"
            f"Lessons: {m['lessons_learned']}"
        )
        h_res = hindsight_service.retain_memory(
            content=h_content,
            metadata={"expert_id": str(exp.id), "project_id": str(prj.id), "source": "handoff"},
            tags=["expert_handoff", m["memory_type"]]
        )

        db_mem = DecisionMemory(
            organization_id=prj.organization_id,
            project_id=prj.id,
            expert_id=exp.id,
            problem=m["problem"],
            context=m["context"],
            options_considered=m["options_considered"],
            decision=m["decision"],
            reasoning=m["reasoning"],
            action_taken=m["action_taken"],
            impact=m["impact"],
            lessons_learned=m["lessons_learned"],
            memory_type=m["memory_type"],
            status="ACTIVE",
            source_type=m["source_type"],
            source_id=f"HANDOFF-{exp.id}-{prj.id}",
            verification_status="VERIFIED",
            outcome_score=0.95,
            hindsight_memory_id=h_res.get("hindsight_memory_id")
        )
        db.add(db_mem)
        db.flush()
        created_mems.append(db_mem)

    db.commit()

    return KnowledgeHandoffResponse(
        status="completed",
        expert_id=exp.id,
        project_id=prj.id,
        created_memories_count=len(created_mems),
        memories=created_mems
    )
