from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Meeting
from app.schemas.schemas import MeetingResponse

router = APIRouter()

@router.get("/meetings", response_model=List[MeetingResponse])
def get_meetings(
    project_id: Optional[int] = Query(None),
    meeting_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Meeting)
    if project_id:
        q = q.filter(Meeting.project_id == project_id)
    if meeting_type:
        q = q.filter(Meeting.meeting_type == meeting_type)
    return q.offset(skip).limit(limit).all()
