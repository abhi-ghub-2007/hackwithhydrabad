from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Technology
from app.schemas.schemas import TechnologyResponse

router = APIRouter()

@router.get("/technologies", response_model=List[TechnologyResponse])
def get_technologies(
    category: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Technology)
    if category:
        q = q.filter(Technology.category == category)
    return q.offset(skip).limit(limit).all()
