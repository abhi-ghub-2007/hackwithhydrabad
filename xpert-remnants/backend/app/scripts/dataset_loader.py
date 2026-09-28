import os
import json
import logging
import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.db.database import Base, engine, SessionLocal
from app.models.models import (
    Organization, Person, Expert, Project, Technology,
    DecisionMemory, Decision, Incident, Lesson, MemoryRelationship
)
from app.services.hindsight_service import hindsight_service
from app.services.batch_processor import batch_processor

logger = logging.getLogger("xpert_remnants.dataset_loader")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DATASET_VERSION = "microsoft-style-v1"

DEFAULT_DATASET_PATHS = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "xpert_remnants_microsoft_style_dataset.json"),
    r"C:\Users\Aboli\Downloads\xpert_remnants_microsoft_style_dataset.json",
    r"c:\hackwithhydrabad\xpert-remnants\backend\data\xpert_remnants_microsoft_style_dataset.json",
    "xpert_remnants_microsoft_style_dataset.json"
]

def find_dataset_file(custom_path: Optional[str] = None) -> str:
    if custom_path and os.path.exists(custom_path):
        return custom_path
    for p in DEFAULT_DATASET_PATHS:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"Canonical dataset file not found in paths: {DEFAULT_DATASET_PATHS}")

def load_raw_dataset(path: Optional[str] = None) -> Dict[str, Any]:
    file_path = find_dataset_file(path)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_dataset(data: Optional[Dict[str, Any]] = None, path: Optional[str] = None) -> Dict[str, Any]:
    """
    Validates the canonical dataset before insertion:
    1. duplicate IDs
    2. missing experts/projects
    3. broken relationships
    4. invalid timestamps
    5. inconsistent project context
    """
    if data is None:
        data = load_raw_dataset(path)

    memories = data.get("memories", [])
    projects = data.get("projects", [])

    proj_ids = {p["project_id"]: p for p in projects}
    expert_ids = {}
    for p in projects:
        for exp in p.get("synthetic_experts", []):
            expert_ids[exp["expert_id"]] = (exp, p["project_id"])

    mem_ids = set()
    dup_ids = []
    missing_proj = []
    missing_exp = []
    broken_rel = []
    invalid_ts = []
    inconsistent_ctx = []

    for m in memories:
        mid = m.get("memory_id")
        if not mid:
            dup_ids.append("MISSING_ID")
        elif mid in mem_ids:
            dup_ids.append(mid)
        else:
            mem_ids.add(mid)

        # 1. Timestamp validation
        ts = m.get("timestamp")
        if not ts:
            invalid_ts.append((mid, "MISSING_TIMESTAMP"))
        else:
            try:
                datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except Exception as e:
                invalid_ts.append((mid, str(ts)))

        # 2. Project & Expert validation
        if "project" in m:
            pid = m["project"].get("project_id")
            if pid not in proj_ids:
                missing_proj.append((mid, pid))
        elif "from_project" in m:
            f_pid = m.get("from_project")
            t_pid = m.get("to_project")
            if f_pid not in proj_ids:
                missing_proj.append((mid, f_pid))
            if t_pid not in proj_ids:
                missing_proj.append((mid, t_pid))

        if "expert" in m:
            eid = m["expert"].get("expert_id")
            if eid not in expert_ids:
                missing_exp.append((mid, eid))
            else:
                exp_info, assigned_pid = expert_ids[eid]
                if "project" in m and m["project"].get("project_id") != assigned_pid:
                    inconsistent_ctx.append((mid, eid, m["project"].get("project_id"), assigned_pid))
        elif "from_expert" in m:
            f_eid = m.get("from_expert")
            t_eid = m.get("to_expert")
            if f_eid not in expert_ids:
                missing_exp.append((mid, f_eid))
            if t_eid not in expert_ids:
                missing_exp.append((mid, t_eid))

    # 3. Relationship integrity
    for m in memories:
        rel = m.get("relationships", {})
        prev = rel.get("previous_memory_id")
        if prev and prev not in mem_ids:
            broken_rel.append((m["memory_id"], "previous_memory_id", prev))
        for dep in rel.get("depends_on", []):
            if dep and dep not in mem_ids:
                broken_rel.append((m["memory_id"], "depends_on", dep))
        sup = rel.get("supersedes")
        if sup and sup not in mem_ids:
            broken_rel.append((m["memory_id"], "supersedes", sup))

    is_valid = (
        len(dup_ids) == 0 and
        len(missing_proj) == 0 and
        len(missing_exp) == 0 and
        len(broken_rel) == 0 and
        len(invalid_ts) == 0 and
        len(inconsistent_ctx) == 0
    )

    result = {
        "dataset_name": data.get("dataset_name"),
        "dataset_version": DATASET_VERSION,
        "is_valid": is_valid,
        "total_records": len(memories),
        "total_projects": len(projects),
        "total_experts": len(expert_ids),
        "validation_errors": {
            "duplicate_ids": dup_ids,
            "missing_projects": missing_proj,
            "missing_experts": missing_exp,
            "broken_relationships": broken_rel,
            "invalid_timestamps": invalid_ts,
            "inconsistent_project_context": inconsistent_ctx
        }
    }

    if is_valid:
        logger.info(f"Dataset validation PASSED: {len(memories)} memories, {len(projects)} projects, {len(expert_ids)} experts.")
    else:
        logger.warning(f"Dataset validation FAILED with errors: {result['validation_errors']}")

    return result

def seed_canonical_dataset(
    db: Session,
    data: Optional[Dict[str, Any]] = None,
    path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Idempotently seeds the canonical dataset into PostgreSQL / SQLite.
    """
    validation = validate_dataset(data, path)
    if not validation["is_valid"]:
        raise ValueError(f"Cannot seed dataset: validation failed: {validation['validation_errors']}")

    if data is None:
        data = load_raw_dataset(path)

    # 1. Ensure target Organization exists
    org = db.query(Organization).filter(Organization.slug == "northstar-india").first()
    if not org:
        org = Organization(
            name="Northstar Technologies India",
            slug="northstar-india",
            domain="northstar.co.in"
        )
        db.add(org)
        db.flush()

    # 2. Map Projects
    project_map: Dict[str, Project] = {}
    for p_data in data.get("projects", []):
        pid = p_data["project_id"]
        p_name = p_data["name"]
        prj = db.query(Project).filter(Project.name == p_name).first()
        if not prj:
            prj = Project(
                organization_id=org.id,
                name=p_name,
                domain=p_data.get("domain", "Enterprise Systems"),
                description=p_data.get("public_basis", "Canonical Benchmark Project"),
                business_context="\n".join(p_data.get("real_public_context", [])),
                status="ACTIVE",
                criticality="HIGH"
            )
            db.add(prj)
            db.flush()
        project_map[pid] = prj

    # 3. Map Technologies
    for p_data in data.get("projects", []):
        for tech_name in p_data.get("technologies", []):
            t = db.query(Technology).filter(Technology.name == tech_name).first()
            if not t:
                t = Technology(
                    name=tech_name,
                    category=p_data.get("domain", "Platform"),
                    description=f"Core technology in {p_data['name']}"
                )
                db.add(t)
                db.flush()

    # 4. Map People and Experts
    expert_map: Dict[str, Expert] = {}
    for p_data in data.get("projects", []):
        prj = project_map[p_data["project_id"]]
        for exp_data in p_data.get("synthetic_experts", []):
            eid = exp_data["expert_id"]
            name = exp_data["name"]
            role = exp_data["role"]
            email = f"{name.lower().replace(' ', '.')}.{eid.lower()}@synthetic.enterprise"

            person = db.query(Person).filter(Person.email == email).first()
            if not person:
                person = Person(
                    full_name=name,
                    email=email,
                    location="Enterprise Center",
                    title=role
                )
                db.add(person)
                db.flush()

            expert = db.query(Expert).filter(Expert.person_id == person.id).first()
            if not expert:
                expert = Expert(
                    person_id=person.id,
                    organization_id=org.id,
                    role=role,
                    department=prj.domain,
                    years_of_experience=8,
                    expertise=f"Architecture & Systems for {prj.name}",
                    biography=f"Synthetic expert for {prj.name} scenarios.",
                    status="FORMER_EMPLOYEE"
                )
                db.add(expert)
                db.flush()
            expert_map[eid] = expert

    # 5. Map Memories idempotently
    existing_mem_keys = set(
        row[0] for row in db.query(DecisionMemory.hindsight_memory_id).all() if row[0]
    )
    existing_source_ids = set(
        row[0] for row in db.query(DecisionMemory.source_id).all() if row[0]
    )

    mem_id_to_db_id: Dict[str, int] = {}
    loaded_records = 0
    duplicate_records = 0
    failed_records = 0

    decisions_loaded = 0
    incidents_loaded = 0
    lessons_loaded = 0

    pending_relationships = []

    # Batch save buffer
    mem_objs = []
    decision_objs = []
    incident_objs = []
    lesson_objs = []

    for m in data.get("memories", []):
        mid = m["memory_id"]
        if mid in existing_mem_keys or mid in existing_source_ids:
            duplicate_records += 1
            # Retrieve existing DB id for relationship resolution
            existing_rec = db.query(DecisionMemory).filter(
                (DecisionMemory.hindsight_memory_id == mid) | (DecisionMemory.source_id == mid)
            ).first()
            if existing_rec:
                mem_id_to_db_id[mid] = existing_rec.id
            continue

        try:
            event = m.get("event", {})
            m_type = event.get("type", "technical_decision")
            timestamp_str = m.get("date") or m.get("timestamp", "")[:10]

            # Resolve project & expert
            if "project" in m:
                prj = project_map[m["project"]["project_id"]]
                exp = expert_map[m["expert"]["expert_id"]]
            else:
                prj = project_map[m["from_project"]]
                exp = expert_map[m["from_expert"]]

            # Format options considered
            options_str = ""
            if "options_considered" in event:
                options_str = "; ".join(
                    f"{opt.get('option_id')}: {opt.get('description')} ({opt.get('status')}) - {opt.get('reason')}"
                    for opt in event["options_considered"]
                )

            # Context
            ctx_data = event.get("context", {})
            if isinstance(ctx_data, dict):
                ctx_str = f"Trigger: {ctx_data.get('trigger', 'Operational Need')}. Constraints: {', '.join(ctx_data.get('constraints', []))}."
            else:
                ctx_str = str(ctx_data) if ctx_data else prj.description

            # Lessons learned & warning
            lesson_text = event.get("lesson") or event.get("reasoning", "")
            if event.get("warning"):
                lesson_text = f"{lesson_text}\nWarning: {event['warning']}"

            # Impact
            outcome_data = event.get("outcome", {})
            impact_text = outcome_data.get("impact") or outcome_data.get("status") or "Stable verification"

            # Artifacts
            artifacts = m.get("artifacts", {})
            source_id = artifacts.get("issue_id") or artifacts.get("pull_request_id") or mid

            db_mem = DecisionMemory(
                organization_id=org.id,
                project_id=prj.id,
                expert_id=exp.id,
                problem=event.get("problem") or event.get("title", "Technical Challenge"),
                context=ctx_str,
                options_considered=options_str,
                decision=event.get("decision") or event.get("title", "Applied Solution"),
                reasoning=event.get("reasoning", "Standardized design pattern applied."),
                action_taken=event.get("experiment", {}).get("hypothesis") or event.get("decision", ""),
                impact=impact_text,
                lessons_learned=lesson_text,
                memory_type=m_type,
                status="ACTIVE",
                source_type=m.get("source", {}).get("type", "SYNTHETIC").upper(),
                source_id=source_id,
                occurred_at=timestamp_str,
                verification_status="VERIFIED",
                outcome_score=float(event.get("confidence", 0.9)),
                hindsight_memory_id=mid
            )
            db.add(db_mem)
            db.flush()
            mem_id_to_db_id[mid] = db_mem.id
            loaded_records += 1

            # Map to Decision table where applicable
            if m_type in ["technical_decision", "decision", "architecture_pattern", "migration"]:
                dec_obj = Decision(
                    project_id=prj.id,
                    expert_id=exp.id,
                    title=event.get("title", f"Decision {mid}"),
                    problem=event.get("problem") or event.get("title", ""),
                    decision=event.get("decision") or event.get("title", ""),
                    reasoning=event.get("reasoning", ""),
                    alternatives=options_str,
                    selected_option=event.get("decision"),
                    rejected_options=options_str,
                    risks=event.get("warning"),
                    expected_outcome=event.get("experiment", {}).get("hypothesis"),
                    actual_outcome=impact_text,
                    decision_date=timestamp_str
                )
                db.add(dec_obj)
                decisions_loaded += 1

            # Map to Incident table where applicable
            if m_type in ["incident", "bug"]:
                inc_obj = Incident(
                    project_id=prj.id,
                    title=event.get("title", f"Incident {mid}"),
                    description=event.get("problem") or event.get("title", ""),
                    severity=outcome_data.get("severity", "HIGH").upper(),
                    root_cause=event.get("problem"),
                    impact=impact_text,
                    detection_method=ctx_str,
                    resolution=event.get("decision"),
                    prevention=event.get("warning") or lesson_text,
                    incident_date=timestamp_str,
                    expert_involved=exp.person.full_name
                )
                db.add(inc_obj)
                incidents_loaded += 1

            # Map to Lesson table where applicable
            if event.get("lesson"):
                les_obj = Lesson(
                    project_id=prj.id,
                    expert_id=exp.id,
                    memory_id=db_mem.id,
                    title=event.get("title", f"Lesson {mid}"),
                    takeaway=event.get("lesson"),
                    category=m_type.upper()
                )
                db.add(les_obj)
                lessons_loaded += 1

            # Queue relationships
            rel_info = m.get("relationships", {})
            if rel_info:
                pending_relationships.append((mid, rel_info))
            elif "relationship" in m:
                pending_relationships.append((mid, {"cross_rel": m["relationship"], "from": m.get("from_project"), "to": m.get("to_project")}))

        except Exception as e:
            logger.error(f"Error seeding memory record {mid}: {e}")
            failed_records += 1

    db.commit()

    # 6. Map Relationships
    relationships_created = 0
    for mid, rel in pending_relationships:
        source_db_id = mem_id_to_db_id.get(mid)
        if not source_db_id:
            continue

        # depends_on
        for dep_mid in rel.get("depends_on", []):
            target_db_id = mem_id_to_db_id.get(dep_mid)
            if target_db_id and target_db_id != source_db_id:
                mr = MemoryRelationship(
                    source_memory_id=source_db_id,
                    target_memory_id=target_db_id,
                    relationship_type="depends_on"
                )
                db.add(mr)
                relationships_created += 1

        # previous_memory_id
        prev_mid = rel.get("previous_memory_id")
        if prev_mid:
            target_db_id = mem_id_to_db_id.get(prev_mid)
            if target_db_id and target_db_id != source_db_id:
                mr = MemoryRelationship(
                    source_memory_id=source_db_id,
                    target_memory_id=target_db_id,
                    relationship_type="follows"
                )
                db.add(mr)
                relationships_created += 1

        # supersedes
        sup_mid = rel.get("supersedes")
        if sup_mid:
            target_db_id = mem_id_to_db_id.get(sup_mid)
            if target_db_id and target_db_id != source_db_id:
                mr = MemoryRelationship(
                    source_memory_id=source_db_id,
                    target_memory_id=target_db_id,
                    relationship_type="supersedes"
                )
                db.add(mr)
                relationships_created += 1

    db.commit()

    summary = {
        "status": "success",
        "dataset_version": DATASET_VERSION,
        "projects_count": len(project_map),
        "experts_count": len(expert_map),
        "loaded_records": loaded_records,
        "duplicate_records": duplicate_records,
        "failed_records": failed_records,
        "decisions_loaded": decisions_loaded,
        "incidents_loaded": incidents_loaded,
        "lessons_loaded": lessons_loaded,
        "relationships_created": relationships_created,
        "total_active_memories_in_db": db.query(DecisionMemory).count()
    }
    logger.info(f"Seeding completed successfully: {summary}")
    return summary

def reset_and_seed(db: Session, path: Optional[str] = None) -> Dict[str, Any]:
    """
    Cleans up canonical benchmark memories and re-seeds freshly.
    """
    logger.info("Executing reset-and-seed: cleaning canonical dataset records...")
    # Delete memories with MEM- prefix in hindsight_memory_id
    canonical_mems = db.query(DecisionMemory).filter(
        DecisionMemory.hindsight_memory_id.like("MEM-%")
    ).all()
    can_ids = [m.id for m in canonical_mems]

    if can_ids:
        db.query(MemoryRelationship).filter(
            (MemoryRelationship.source_memory_id.in_(can_ids)) |
            (MemoryRelationship.target_memory_id.in_(can_ids))
        ).delete(synchronize_session=False)

        db.query(Lesson).filter(Lesson.memory_id.in_(can_ids)).delete(synchronize_session=False)
        db.query(DecisionMemory).filter(DecisionMemory.id.in_(can_ids)).delete(synchronize_session=False)
        db.commit()

    return seed_canonical_dataset(db, path=path)

def sync_dataset_to_hindsight(db: Session, bank_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Syncs approved active memories to Hindsight using the existing retain_batch.
    Preserves all 8 required metadata fields.
    """
    memories = db.query(DecisionMemory).filter(DecisionMemory.status == "ACTIVE").all()
    logger.info(f"Preparing {len(memories)} active memories for Hindsight retention...")

    mem_dicts = [
        {
            "id": m.id,
            "problem": m.problem,
            "context": m.context,
            "decision": m.decision,
            "reasoning": m.reasoning,
            "action_taken": m.action_taken,
            "impact": m.impact,
            "lessons_learned": m.lessons_learned,
            "project_id": m.project_id,
            "expert_id": m.expert_id,
            "memory_id": m.hindsight_memory_id or str(m.id),
            "memory_type": m.memory_type,
            "occurred_at": m.occurred_at,
            "technology": m.project.name if m.project else "Enterprise System",
            "confidence": m.outcome_score,
            "verification_status": m.verification_status,
            "status": m.status
        }
        for m in memories
    ]

    target_bank = bank_id or settings.HINDSIGHT_BANK_ID
    res = batch_processor.process_memories(mem_dicts, bank_id=target_bank)
    return res

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Canonical Dataset Ingestion & Validation Tool")
    parser.add_argument("command", choices=["validate", "seed", "reset-and-seed", "sync-hindsight"], help="Action to execute")
    parser.add_argument("--path", type=str, default=None, help="Path to canonical dataset json")
    parser.add_argument("--bank", type=str, default=None, help="Target Hindsight bank ID")

    args = parser.parse_args()
    db = SessionLocal()
    try:
        if args.command == "validate":
            res = validate_dataset(path=args.path)
            print(json.dumps(res, indent=2))
        elif args.command == "seed":
            res = seed_canonical_dataset(db, path=args.path)
            print(json.dumps(res, indent=2))
        elif args.command == "reset-and-seed":
            res = reset_and_seed(db, path=args.path)
            print(json.dumps(res, indent=2))
        elif args.command == "sync-hindsight":
            res = sync_dataset_to_hindsight(db, bank_id=args.bank)
            print(json.dumps(res, indent=2))
    finally:
        db.close()
