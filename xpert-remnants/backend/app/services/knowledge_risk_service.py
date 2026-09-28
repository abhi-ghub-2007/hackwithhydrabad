from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.models import KnowledgeRisk, Project, Expert, DecisionMemory

class KnowledgeRiskService:
    """
    Computes organizational knowledge risks based on single-expert dependency,
    system criticality, documentation coverage, and absence of secondary experts (Section 36).
    """

    @staticmethod
    def calculate_risk_level(
        criticality: str,
        documentation_coverage: float,
        verification_level: float,
        has_backup: bool
    ) -> str:
        """
        Determines overall risk level (HIGH, MEDIUM, LOW).
        """
        score = 0.0
        if criticality == "CRITICAL":
            score += 4.0
        elif criticality == "HIGH":
            score += 2.5
        else:
            score += 1.0

        # Penalize low documentation coverage
        if documentation_coverage < 0.4:
            score += 3.0
        elif documentation_coverage < 0.7:
            score += 1.5

        # Penalize lack of verification
        if verification_level < 0.5:
            score += 2.0

        # Penalize single point of failure (no backup expert)
        if not has_backup:
            score += 3.5

        if score >= 8.0:
            return "HIGH"
        elif score >= 5.0:
            return "MEDIUM"
        return "LOW"

    @classmethod
    def get_project_risks(cls, db: Session, project_id: int) -> List[Dict[str, Any]]:
        risks = db.query(KnowledgeRisk).filter(KnowledgeRisk.project_id == project_id).all()
        results = []
        for r in risks:
            exp = db.query(Expert).filter(Expert.id == r.expert_id).first()
            exp_name = exp.person.full_name if exp and exp.person else "Unknown Expert"
            prj = db.query(Project).filter(Project.id == r.project_id).first()
            prj_name = prj.name if prj else "Unknown Project"

            results.append({
                "id": r.id,
                "project_id": r.project_id,
                "expert_id": r.expert_id,
                "topic": r.topic,
                "risk_level": r.risk_level,
                "criticality": r.criticality,
                "documentation_coverage": r.documentation_coverage,
                "verification_level": r.verification_level,
                "action_required": r.action_required,
                "expert_name": exp_name,
                "project_name": prj_name
            })
        return results

    @classmethod
    def get_all_risks(cls, db: Session) -> List[Dict[str, Any]]:
        risks = db.query(KnowledgeRisk).all()
        results = []
        for r in risks:
            exp = db.query(Expert).filter(Expert.id == r.expert_id).first()
            exp_name = exp.person.full_name if exp and exp.person else "Unknown Expert"
            prj = db.query(Project).filter(Project.id == r.project_id).first()
            prj_name = prj.name if prj else "Unknown Project"

            results.append({
                "id": r.id,
                "project_id": r.project_id,
                "expert_id": r.expert_id,
                "topic": r.topic,
                "risk_level": r.risk_level,
                "criticality": r.criticality,
                "documentation_coverage": r.documentation_coverage,
                "verification_level": r.verification_level,
                "action_required": r.action_required,
                "expert_name": exp_name,
                "project_name": prj_name
            })
        return results

knowledge_risk_service = KnowledgeRiskService()
