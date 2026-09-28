import sys, os
sys.path.insert(0, os.path.abspath("."))
from app.db.database import SessionLocal
from app.models.models import DecisionMemory, Project

def main():
    db = SessionLocal()
    prj = db.query(Project).filter(Project.name == "Project X").first()
    if not prj:
        print("No Project X found.")
        return
    mems = db.query(DecisionMemory).filter(DecisionMemory.project_id == prj.id).all()
    print(f"Project X id={prj.id}, count={len(mems)}")
    for m in mems:
        print(f"id={m.id}, is_curr={m.is_current}, status={m.decision_status}, supersedes={m.supersedes_memory_id}, decision='{m.decision[:60]}'")

if __name__ == "__main__":
    main()
