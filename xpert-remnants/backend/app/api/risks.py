from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import KnowledgeRiskResponse
from app.services.knowledge_risk_service import knowledge_risk_service

router = APIRouter()

@router.get("/risks", response_model=List[KnowledgeRiskResponse])
def get_all_knowledge_risks(db: Session = Depends(get_db)):
    """
    Returns all enterprise knowledge risks across projects and experts (Section 36 & 38).
    """
    return knowledge_risk_service.get_all_risks(db)
