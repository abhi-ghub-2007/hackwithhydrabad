import sys, os
sys.path.insert(0, os.path.abspath("."))
from app.db.database import SessionLocal
from app.models.models import DecisionMemory, Project, MemoryRelationship

def main():
    db = SessionLocal()
    prj = db.query(Project).filter(Project.name == "Project X").first()
    if not prj:
        return
    # Delete temporary test rows created during test runs for Project X
    test_mems = db.query(DecisionMemory).filter(
        DecisionMemory.project_id == prj.id,
        DecisionMemory.id > 100001
    ).all()
    for m in test_mems:
        db.query(MemoryRelationship).filter(
            (MemoryRelationship.source_memory_id == m.id) | (MemoryRelationship.target_memory_id == m.id)
        ).delete(synchronize_session=False)
        db.delete(m)
    
    # Restore baseline
    base = db.query(DecisionMemory).filter(DecisionMemory.id == 100001).first()
    if base:
        base.is_current = True
        base.decision_status = "REJECTED"
        base.status = "HISTORICAL"
        base.supersedes_memory_id = None
        db.add(base)
    db.commit()
    print("Cleaned up Project X test records and restored baseline.")

if __name__ == "__main__":
    main()
