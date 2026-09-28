from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Decision, DecisionMemory, Project, Expert
from app.schemas.schemas import DecisionResponse, DecisionReplayResponse, DecisionReplayStep

router = APIRouter()

@router.get("/decisions", response_model=List[DecisionResponse])
def get_decisions(
    project_id: Optional[int] = Query(None),
    expert_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Decision)
    if project_id:
        q = q.filter(Decision.project_id == project_id)
    if expert_id:
        q = q.filter(Decision.expert_id == expert_id)
    return q.offset(skip).limit(limit).all()

@router.get("/decisions/{decision_id}", response_model=DecisionReplayResponse)
def get_decision_replay(decision_id: int, db: Session = Depends(get_db)):
    """
    Decision Replay endpoint (Section 39):
    Transforms preserved historical decision into a chronological 6-stage timeline view:
    Problem detected -> Investigation & Options -> Decision -> Action -> Outcome -> Lesson.
    """
    decision = db.query(Decision).filter(Decision.id == decision_id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")

    prj = db.query(Project).filter(Project.id == decision.project_id).first()
    exp = db.query(Expert).filter(Expert.id == decision.expert_id).first()

    prj_name = prj.name if prj else "Enterprise System"
    exp_name = exp.person.full_name if exp and exp.person else "Lead Architect"

    steps = [
        DecisionReplayStep(
            step_number=1,
            stage="Problem Detected",
            title="Operational Degradation Triggered Alert",
            description=decision.problem,
            timestamp=decision.decision_date or "Day 0",
            actor=exp_name,
            status="completed"
        ),
        DecisionReplayStep(
            step_number=2,
            stage="Investigation & Options Evaluated",
            title="Exploration of Alternatives & Trade-offs",
            description=f"Alternatives: {decision.alternatives or 'Evaluated multiple horizontal and vertical scaling paths.'} | Rejected: {decision.rejected_options or 'Rejected approaches that violated DB capacity.'}",
            timestamp=decision.decision_date or "Day 0 + 2h",
            actor=exp_name,
            status="completed"
        ),
        DecisionReplayStep(
            step_number=3,
            stage="Decision Formulated",
            title="Formal Architectural Selection",
            description=f"Selected: {decision.decision} | Rationale: {decision.reasoning}",
            timestamp=decision.decision_date or "Day 0 + 4h",
            actor=exp_name,
            status="completed"
        ),
        DecisionReplayStep(
            step_number=4,
            stage="Action Executed",
            title="Production Rollout & Canary Verification",
            description=f"Deployed updated configurations and verified telemetry monitors under active load.",
            timestamp=decision.decision_date or "Day 0 + 6h",
            actor=exp_name,
            status="completed"
        ),
        DecisionReplayStep(
            step_number=5,
            stage="Realized Outcome",
            title="Telemetry Impact & SLA Verification",
            description=f"Expected: {decision.expected_outcome or 'Stabilize P99 latency.'} | Actual: {decision.actual_outcome or 'Significant latency reduction without downtime.'}",
            timestamp=decision.decision_date or "Day 1",
            actor=exp_name,
            status="completed"
        ),
        DecisionReplayStep(
            step_number=6,
            stage="Lessons Learned & Warnings",
            title="Organizational Memory Retention",
            description=f"Operational Warning: Always verify database max_connections headroom before increasing application-side pools.",
            timestamp=decision.decision_date or "Postmortem",
            actor=exp_name,
            status="completed"
        )
    ]

    return DecisionReplayResponse(
        decision_id=decision.id,
        title=decision.title,
        project_name=prj_name,
        expert_name=exp_name,
        decision_date=decision.decision_date,
        steps=steps
    )
