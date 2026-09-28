from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Incident
from app.schemas.schemas import IncidentResponse

router = APIRouter()

@router.get("/incidents", response_model=List[IncidentResponse])
def get_incidents(
    project_id: Optional[int] = Query(None),
    severity: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Incident)
    if project_id:
        q = q.filter(Incident.project_id == project_id)
    if severity:
        q = q.filter(Incident.severity == severity)
    return q.offset(skip).limit(limit).all()

@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return inc
