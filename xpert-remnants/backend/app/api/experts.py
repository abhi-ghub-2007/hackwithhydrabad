from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Expert, Person
from app.schemas.schemas import ExpertResponse, PersonResponse

router = APIRouter()

@router.get("/experts", response_model=List[ExpertResponse])
def get_experts(
    department: str = Query(None),
    status: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Expert)
    if department:
        q = q.filter(Expert.department == department)
    if status:
        q = q.filter(Expert.status == status)
    return q.offset(skip).limit(limit).all()

@router.get("/experts/{expert_id}", response_model=ExpertResponse)
def get_expert(expert_id: int, db: Session = Depends(get_db)):
    expert = db.query(Expert).filter(Expert.id == expert_id).first()
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    return expert

@router.get("/people", response_model=List[PersonResponse])
def get_people(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return db.query(Person).offset(skip).limit(limit).all()
