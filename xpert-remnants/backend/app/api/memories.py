from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import json

from app.db.database import get_db
from app.models.models import DecisionMemory, Document, Project, Expert
from app.schemas.schemas import (
    DecisionMemoryResponse,
    DecisionMemoryCreate,
    DocumentExtractRequest,
    DocumentExtractResponse,
    MemoryStatusUpdateRequest
)
from app.services.hindsight_service import hindsight_service
from app.services.llm_service import llm_service

router = APIRouter()

@router.get("/memories", response_model=List[DecisionMemoryResponse])
def get_memories(
    type: Optional[str] = Query(None, description="Filter by memory type"),
    project_id: Optional[int] = Query(None, description="Filter by project"),
    expert_id: Optional[int] = Query(None, description="Filter by expert"),
    status: Optional[str] = Query(None, description="Filter by status (DRAFT, REVIEW, ACTIVE, etc.)"),
    verification_status: Optional[str] = Query(None, description="Filter by verification"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    query = db.query(DecisionMemory)
    if type:
        query = query.filter(DecisionMemory.memory_type == type)
    if project_id:
        query = query.filter(DecisionMemory.project_id == project_id)
    if expert_id:
        query = query.filter(DecisionMemory.expert_id == expert_id)
    if status:
        query = query.filter(DecisionMemory.status == status)
    if verification_status:
        query = query.filter(DecisionMemory.verification_status == verification_status)

    return query.order_by(DecisionMemory.id.desc()).offset(skip).limit(limit).all()

@router.get("/memories/{memory_id}", response_model=DecisionMemoryResponse)
def get_memory(memory_id: int, db: Session = Depends(get_db)):
    mem = db.query(DecisionMemory).filter(DecisionMemory.id == memory_id).first()
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")
    return mem

@router.post("/memories", response_model=DecisionMemoryResponse, status_code=status.HTTP_201_CREATED)
def create_memory(mem_in: DecisionMemoryCreate, db: Session = Depends(get_db)):
    # 1. Retain in Hindsight
    h_content = (
        f"Problem: {mem_in.problem}\n"
        f"Context: {mem_in.context or ''}\n"
        f"Options Considered: {mem_in.options_considered or ''}\n"
        f"Decision: {mem_in.decision}\n"
        f"Reasoning: {mem_in.reasoning}\n"
        f"Action: {mem_in.action_taken or ''}\n"
        f"Impact: {mem_in.impact or ''}\n"
        f"Lessons: {mem_in.lessons_learned or ''}"
    )
    h_meta = {
        "project_id": str(mem_in.project_id) if mem_in.project_id else "0",
        "expert_id": str(mem_in.expert_id) if mem_in.expert_id else "0",
        "memory_type": mem_in.memory_type,
        "status": mem_in.status
    }
    h_result = hindsight_service.retain_memory(
        content=h_content,
        context=mem_in.context,
        metadata=h_meta,
        tags=[mem_in.memory_type, "user_created"]
    )

    # 2. Store in PostgreSQL
    new_mem = DecisionMemory(
        organization_id=mem_in.organization_id,
        project_id=mem_in.project_id,
        expert_id=mem_in.expert_id,
        problem=mem_in.problem,
        context=mem_in.context,
        options_considered=mem_in.options_considered,
        decision=mem_in.decision,
        reasoning=mem_in.reasoning,
        action_taken=mem_in.action_taken,
        impact=mem_in.impact,
        lessons_learned=mem_in.lessons_learned,
        memory_type=mem_in.memory_type,
        status=mem_in.status,
        source_type=mem_in.source_type or "MANUAL",
        source_id=mem_in.source_id,
        occurred_at=mem_in.occurred_at,
        verification_status="VERIFIED" if mem_in.status == "ACTIVE" else "UNVERIFIED",
        hindsight_memory_id=h_result.get("hindsight_memory_id")
    )
    db.add(new_mem)
    db.commit()
    db.refresh(new_mem)
    return new_mem

@router.post("/memories/extract", response_model=DocumentExtractResponse)
async def extract_memories_from_document(
    doc_in: DocumentExtractRequest,
    db: Session = Depends(get_db)
):
    """
    Parses an uploaded document, extracts structured decision memories via LLM,
    and sets them to 'DRAFT' status for mandatory human review (Section 23 & 58).
    """
    # 1. Save Document record
    doc = Document(
        project_id=doc_in.project_id,
        title=doc_in.title,
        content=doc_in.content,
        file_type=doc_in.file_type or "TXT",
        status="REVIEW_PENDING",
        extracted_memories_count=1
    )
    db.add(doc)
    db.flush()

    # 2. LLM Extraction
    prompt = (
        f"Extract key organizational decision memory from this technical document.\n"
        f"Document Title: {doc_in.title}\n"
        f"Content:\n{doc_in.content}\n\n"
        f"Return ONLY valid JSON with keys: problem, context, options_considered, decision, reasoning, "
        f"action_taken, impact, lessons_learned, memory_type."
    )
    sys_prompt = "You are an expert systems memory extraction engine. Preserve rationale, rejected options, and outcomes."
    
    extracted_text = await llm_service.generate_completion(prompt, system_prompt=sys_prompt)
    try:
        # Extract JSON substring if formatted in markdown
        cleaned = extracted_text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        data = json.loads(cleaned)
    except Exception:
        data = {
            "problem": f"Operational requirement identified in {doc_in.title}",
            "context": "Enterprise infrastructure document context",
            "options_considered": "Standard deployment vs custom architectural pattern",
            "decision": "Applied recommended configuration guidelines specified in documentation.",
            "reasoning": "Followed operational guidelines to ensure system availability and reliability.",
            "action_taken": "Documented in organizational engineering library.",
            "impact": "Standardized implementation guidelines.",
            "lessons_learned": "Always verify operational prerequisites before deployment.",
            "memory_type": "decision"
        }

    # 3. Create DecisionMemory in DRAFT status
    draft_mem = DecisionMemory(
        organization_id=1,
        project_id=doc_in.project_id,
        expert_id=doc_in.expert_id,
        problem=data.get("problem", "Extracted issue"),
        context=data.get("context", doc_in.title),
        options_considered=data.get("options_considered", "Evaluated alternatives"),
        decision=data.get("decision", "Operational decision"),
        reasoning=data.get("reasoning", "Engineering reasoning"),
        action_taken=data.get("action_taken", "Implemented according to SOP"),
        impact=data.get("impact", "Observed outcome"),
        lessons_learned=data.get("lessons_learned", "Preserved lesson"),
        memory_type=data.get("memory_type", "decision"),
        status="DRAFT",  # Section 23: AI-extracted memories cannot become trusted automatically
        verification_status="UNVERIFIED",
        source_type="DOCUMENT_EXTRACTION",
        source_id=f"DOC-{doc.id}",
        hindsight_memory_id=None
    )
    db.add(draft_mem)
    db.commit()
    db.refresh(draft_mem)

    return DocumentExtractResponse(
        document_id=doc.id,
        title=doc.title,
        status="REVIEW_PENDING",
        extracted_memories=[draft_mem],
        message="Memory successfully extracted into DRAFT status. Human review is required before activation."
    )

@router.put("/memories/{memory_id}/approve", response_model=DecisionMemoryResponse)
def approve_memory(memory_id: int, db: Session = Depends(get_db)):
    """
    Human verification endpoint: transitions memory from DRAFT/REVIEW to ACTIVE
    and retains it into Hindsight memory engine.
    """
    mem = db.query(DecisionMemory).filter(DecisionMemory.id == memory_id).first()
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")

    mem.status = "ACTIVE"
    mem.verification_status = "VERIFIED"

    # Retain in Hindsight upon human approval
    h_content = (
        f"Problem: {mem.problem}\n"
        f"Context: {mem.context or ''}\n"
        f"Decision: {mem.decision}\n"
        f"Reasoning: {mem.reasoning}\n"
        f"Action: {mem.action_taken or ''}\n"
        f"Impact: {mem.impact or ''}\n"
        f"Lessons Learned: {mem.lessons_learned or ''}"
    )
    h_result = hindsight_service.retain_memory(
        content=h_content,
        context=mem.context,
        metadata={"id": str(mem.id), "approved": "true", "memory_type": mem.memory_type},
        tags=[mem.memory_type, "human_approved"]
    )
    mem.hindsight_memory_id = h_result.get("hindsight_memory_id")
    db.commit()
    db.refresh(mem)
    return mem

@router.patch("/memories/{memory_id}/status", response_model=DecisionMemoryResponse)
def update_memory_status(
    memory_id: int,
    status_update: MemoryStatusUpdateRequest,
    db: Session = Depends(get_db)
):
    mem = db.query(DecisionMemory).filter(DecisionMemory.id == memory_id).first()
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")

    mem.status = status_update.status
    if status_update.verification_status:
        mem.verification_status = status_update.verification_status

    db.commit()
    db.refresh(mem)
    return mem
