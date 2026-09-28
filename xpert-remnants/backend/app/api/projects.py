from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Project, KnowledgeRisk, Decision, Incident, DecisionMemory, Expert, ProjectModule
from app.schemas.schemas import ProjectResponse, KnowledgeRiskResponse, KnowledgeMapResponse, KnowledgeMapNode, KnowledgeMapEdge, ProjectModuleResponse
from app.services.knowledge_risk_service import knowledge_risk_service

router = APIRouter()

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(
    domain: str = Query(None),
    status: str = Query(None),
    canonical_only: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Project)
    if canonical_only:
        q = q.filter(Project.id.in_([10, 11, 12, 13, 14]))
    if domain:
        q = q.filter(Project.domain == domain)
    if status:
        q = q.filter(Project.status == status)
    return q.offset(skip).limit(limit).all()

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    prj = db.query(Project).filter(Project.id == project_id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")
    return prj

@router.get("/projects/{project_id}/modules", response_model=List[ProjectModuleResponse])
def get_project_modules(project_id: int, db: Session = Depends(get_db)):
    prj = db.query(Project).filter(Project.id == project_id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(ProjectModule).filter(ProjectModule.project_id == project_id).all()

@router.get("/projects/{project_id}/knowledge-risks", response_model=List[KnowledgeRiskResponse])
def get_project_knowledge_risks(project_id: int, db: Session = Depends(get_db)):
    prj = db.query(Project).filter(Project.id == project_id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")
    return knowledge_risk_service.get_project_risks(db, project_id)

@router.get("/projects/{project_id}/knowledge-map", response_model=KnowledgeMapResponse)
def get_project_knowledge_map(project_id: int, db: Session = Depends(get_db)):
    """
    Returns graph representation of project entities: experts, decisions, incidents, and technologies (Section 40).
    """
    prj = db.query(Project).filter(Project.id == project_id).first()
    if not prj:
        raise HTTPException(status_code=404, detail="Project not found")

    nodes = [KnowledgeMapNode(id=f"proj-{prj.id}", label=prj.name, type="project", group="Project")]
    edges = []

    # Get decisions
    decisions = db.query(Decision).filter(Decision.project_id == project_id).all()
    for d in decisions:
        node_id = f"dec-{d.id}"
        nodes.append(KnowledgeMapNode(id=node_id, label=d.title, type="decision", group="Decisions"))
        edges.append(KnowledgeMapEdge(source=f"proj-{prj.id}", target=node_id, label="contains"))

        # Expert link
        exp = db.query(Expert).filter(Expert.id == d.expert_id).first()
        if exp and exp.person:
            exp_node = f"exp-{exp.id}"
            if not any(n.id == exp_node for n in nodes):
                nodes.append(KnowledgeMapNode(id=exp_node, label=exp.person.full_name, type="expert", group="Experts"))
            edges.append(KnowledgeMapEdge(source=exp_node, target=node_id, label="authored"))

    # Get incidents
    incidents = db.query(Incident).filter(Incident.project_id == project_id).all()
    for inc in incidents:
        node_id = f"inc-{inc.id}"
        nodes.append(KnowledgeMapNode(id=node_id, label=inc.title, type="incident", group="Incidents"))
        edges.append(KnowledgeMapEdge(source=f"proj-{prj.id}", target=node_id, label="experienced"))

    return KnowledgeMapResponse(nodes=nodes, edges=edges)
