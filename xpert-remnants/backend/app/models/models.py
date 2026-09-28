import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean, Enum
)
from sqlalchemy.orm import relationship
from app.db.database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    domain = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    users = relationship("User", back_populates="organization")
    projects = relationship("Project", back_populates="organization")
    experts = relationship("Expert", back_populates="organization")
    memories = relationship("DecisionMemory", back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="EMPLOYEE")  # ADMIN, MANAGER, EXPERT, EMPLOYEE
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    organization = relationship("Organization", back_populates="users")


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    location = Column(String(100), nullable=True)  # Pune, Mumbai, Bengaluru, etc.
    title = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    expert_profile = relationship("Expert", back_populates="person", uselist=False)


class Expert(Base):
    __tablename__ = "experts"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    role = Column(String(100), nullable=False)  # e.g., Principal Software Architect
    department = Column(String(100), nullable=False)  # Engineering, Payments, Platform
    years_of_experience = Column(Integer, default=5)
    expertise = Column(Text, nullable=True)  # JSON or CSV list of skills
    biography = Column(Text, nullable=True)
    joining_date = Column(String(20), nullable=True)
    leaving_date = Column(String(20), nullable=True)
    status = Column(String(50), default="FORMER_EMPLOYEE")  # ACTIVE, FORMER_EMPLOYEE, ON_LEAVE
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    person = relationship("Person", back_populates="expert_profile")
    organization = relationship("Organization", back_populates="experts")
    project = relationship("Project", backref="experts")
    memories = relationship("DecisionMemory", back_populates="expert")
    decisions = relationship("Decision", back_populates="expert")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    domain = Column(String(100), nullable=True)  # Payments, Platform, Auth, Data
    business_context = Column(Text, nullable=True)
    status = Column(String(50), default="ACTIVE")
    start_date = Column(String(20), nullable=True)
    end_date = Column(String(20), nullable=True)
    criticality = Column(String(50), default="HIGH")  # HIGH, MEDIUM, LOW
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    organization = relationship("Organization", back_populates="projects")
    memories = relationship("DecisionMemory", back_populates="project")
    decisions = relationship("Decision", back_populates="project")
    incidents = relationship("Incident", back_populates="project")
    meetings = relationship("Meeting", back_populates="project")
    documents = relationship("Document", back_populates="project")


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=True)  # Database, Message Queue, Framework
    description = Column(Text, nullable=True)
    version_or_generation = Column(String(50), nullable=True)


class DecisionMemory(Base):
    __tablename__ = "decision_memories"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=True)
    
    problem = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    options_considered = Column(Text, nullable=True)
    decision = Column(Text, nullable=False)
    reasoning = Column(Text, nullable=False)
    action_taken = Column(Text, nullable=True)
    impact = Column(Text, nullable=True)
    lessons_learned = Column(Text, nullable=True)
    
    memory_type = Column(String(50), default="decision")  
    # decision, mistake, failure, warning, lesson, incident, experience, observation, rejected_approach, constraint, tradeoff, outcome
    
    status = Column(String(50), default="ACTIVE")  
    # DRAFT, REVIEW, ACTIVE, REVIEW_REQUIRED, UPDATED, ARCHIVED
    
    source_type = Column(String(100), nullable=True)  # INCIDENT, ARCHITECTURE_REVIEW, HANDOFF, MANUAL, POSTMORTEM
    source_id = Column(String(100), nullable=True)    # e.g., INC-1842, DEC-219
    occurred_at = Column(String(50), nullable=True)   # e.g., 2023-11-14
    
    verification_status = Column(String(50), default="VERIFIED")  # VERIFIED, UNVERIFIED, CONTRADICTED
    outcome_score = Column(Float, default=1.0)
    hindsight_memory_id = Column(String(255), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Decision Evolution & Provenance Fields (Antigravity 3.8 Flash)
    decision_status = Column(String(50), default="ACTIVE")  # ACTIVE, REJECTED, SUPERSEDED, HISTORICAL
    effective_at = Column(String(50), nullable=True)        # Effective date string e.g. 2026-09-28
    supersedes_memory_id = Column(Integer, ForeignKey("decision_memories.id"), nullable=True)
    change_reason = Column(Text, nullable=True)             # Why the decision changed
    changed_by_user_id = Column(String(100), nullable=True) # Who changed it (e.g., current authorized user)
    change_type = Column(String(50), nullable=True)         # REQUIREMENTS_CHANGE, DIRECTIVE, EVALUATION
    is_current = Column(Boolean, default=True)              # Whether this is the active decision for the topic

    organization = relationship("Organization", back_populates="memories")
    project = relationship("Project", back_populates="memories")
    expert = relationship("Expert", back_populates="memories")


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=False)
    title = Column(String(255), nullable=False)
    problem = Column(Text, nullable=False)
    decision = Column(Text, nullable=False)
    reasoning = Column(Text, nullable=False)
    alternatives = Column(Text, nullable=True)
    selected_option = Column(Text, nullable=True)
    rejected_options = Column(Text, nullable=True)
    risks = Column(Text, nullable=True)
    expected_outcome = Column(Text, nullable=True)
    actual_outcome = Column(Text, nullable=True)
    decision_date = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="decisions")
    expert = relationship("Expert", back_populates="decisions")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), default="CRITICAL")  # CRITICAL, HIGH, MEDIUM, LOW
    root_cause = Column(Text, nullable=True)
    impact = Column(Text, nullable=True)
    detection_method = Column(Text, nullable=True)
    resolution = Column(Text, nullable=True)
    prevention = Column(Text, nullable=True)
    incident_date = Column(String(20), nullable=True)
    expert_involved = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="incidents")


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    date = Column(String(20), nullable=True)
    meeting_type = Column(String(100), nullable=True)  # Incident Review, Architecture Review
    participants = Column(Text, nullable=True)
    discussion_summary = Column(Text, nullable=True)
    decisions_made = Column(Text, nullable=True)
    action_items = Column(Text, nullable=True)
    outcomes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="meetings")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    file_type = Column(String(50), default="TXT")  # PDF, DOCX, TXT, MD
    source_url = Column(String(255), nullable=True)
    status = Column(String(50), default="PROCESSED")  # UPLOADED, PROCESSED, REVIEW_PENDING
    extracted_memories_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="documents")


class KnowledgeRisk(Base):
    __tablename__ = "knowledge_risks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=False)
    topic = Column(String(255), nullable=False)
    risk_level = Column(String(50), default="HIGH")  # HIGH, MEDIUM, LOW
    criticality = Column(String(50), default="CRITICAL")
    documentation_coverage = Column(Float, default=0.3)  # 0.0 to 1.0
    verification_level = Column(Float, default=0.4)
    backup_expert_id = Column(Integer, nullable=True)
    action_required = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False)
    actor_id = Column(Integer, nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    metadata_json = Column(Text, nullable=True)


class MemoryRelationship(Base):
    __tablename__ = "memory_relationships"

    id = Column(Integer, primary_key=True, index=True)
    source_memory_id = Column(Integer, ForeignKey("decision_memories.id"), nullable=False)
    target_memory_id = Column(Integer, ForeignKey("decision_memories.id"), nullable=False)
    relationship_type = Column(String(100), nullable=False)  
    # related_to, caused_by, resulted_in, contradicts, follows, references, learned_from


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    lead_expert_id = Column(Integer, ForeignKey("experts.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=True)
    memory_id = Column(Integer, ForeignKey("decision_memories.id"), nullable=True)
    title = Column(String(255), nullable=False)
    takeaway = Column(Text, nullable=False)
    category = Column(String(100), default="OPERATIONAL")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, default=1)
    ask_query = Column(Text, nullable=False)
    feedback_type = Column(String(50), nullable=False)  # HELPFUL, PARTIALLY_HELPFUL, NOT_HELPFUL
    actual_result = Column(Text, nullable=True)
    decision_memory_id = Column(Integer, ForeignKey("decision_memories.id"), nullable=True)
    hindsight_memory_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ProjectModule(Base):
    __tablename__ = "project_modules"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    technology = Column(String(255), nullable=True)
    dependencies = Column(Text, nullable=True)
    risks = Column(Text, nullable=True)
    current_state = Column(String(100), default="ACTIVE")
    provenance = Column(String(100), default="VERIFIED_PUBLIC")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", backref="modules")


class KnowledgeUpdate(Base):
    __tablename__ = "knowledge_updates"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    update_type = Column(String(100), default="DECISION_CHANGE")  # DECISION_CHANGE, ARCHITECTURE_CHANGE, OUTCOME, CORRECTION
    old_state = Column(Text, nullable=True)
    new_state = Column(Text, nullable=False)
    reason = Column(Text, nullable=True)
    actor = Column(String(255), default="current_user")
    effective_at = Column(String(50), nullable=True)
    confidence = Column(Float, default=1.0)
    source = Column(String(100), default="user_dialogue")
    provenance = Column(String(100), default="USER_UPDATE")
    related_decision_id = Column(Integer, ForeignKey("decision_memories.id"), nullable=True)
    related_memory_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project")


class LearningEvent(Base):
    __tablename__ = "learning_events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    event_type = Column(String(100), nullable=False)  # DECISION, CORRECTION, OUTCOME, LESSON, FEEDBACK
    source = Column(String(100), default="user_dialogue")
    content = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    promotion_status = Column(String(50), default="PERSISTED")  # EPHEMERAL, CANDIDATE, CONFIRMED, PERSISTED, SUPERSEDED
    promoted_decision_id = Column(Integer, ForeignKey("decision_memories.id"), nullable=True)
    promoted_memory_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project")

