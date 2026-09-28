from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
import datetime

class HealthResponse(BaseModel):
    status: str
    application: str
    environment: Optional[str] = None
    hindsight_configured: bool = False
    llm_configured: bool = False

class OrganizationBase(BaseModel):
    name: str
    slug: str
    domain: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class PersonBase(BaseModel):
    full_name: str
    email: str
    location: Optional[str] = None
    title: Optional[str] = None

class PersonResponse(PersonBase):
    id: int
    created_at: Optional[datetime.datetime] = None
    model_config = ConfigDict(from_attributes=True)

class ExpertBase(BaseModel):
    role: str
    department: str
    years_of_experience: int = 5
    expertise: Optional[str] = None
    biography: Optional[str] = None
    joining_date: Optional[str] = None
    leaving_date: Optional[str] = None
    status: str = "FORMER_EMPLOYEE"

class ExpertResponse(ExpertBase):
    id: int
    person_id: int
    organization_id: int
    person: Optional[PersonResponse] = None
    model_config = ConfigDict(from_attributes=True)

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    domain: Optional[str] = None
    business_context: Optional[str] = None
    status: str = "ACTIVE"
    criticality: str = "HIGH"

class ProjectResponse(ProjectBase):
    id: int
    organization_id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class TechnologyResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    version_or_generation: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class DecisionMemoryBase(BaseModel):
    problem: str
    context: Optional[str] = None
    options_considered: Optional[str] = None
    decision: str
    reasoning: str
    action_taken: Optional[str] = None
    impact: Optional[str] = None
    lessons_learned: Optional[str] = None
    memory_type: str = "decision"
    # decision, mistake, failure, warning, lesson, incident, experience, observation, rejected_approach, constraint, tradeoff, outcome
    status: str = "ACTIVE"
    # DRAFT, REVIEW, ACTIVE, REVIEW_REQUIRED, UPDATED, ARCHIVED
    source_type: Optional[str] = "MANUAL"
    source_id: Optional[str] = None
    occurred_at: Optional[str] = None

class DecisionMemoryCreate(DecisionMemoryBase):
    organization_id: int = 1
    project_id: Optional[int] = None
    expert_id: Optional[int] = None

class DecisionMemoryResponse(DecisionMemoryBase):
    id: int
    organization_id: int
    project_id: Optional[int] = None
    expert_id: Optional[int] = None
    verification_status: str = "VERIFIED"
    outcome_score: float = 1.0
    hindsight_memory_id: Optional[str] = None
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class DecisionResponse(BaseModel):
    id: int
    project_id: int
    expert_id: int
    title: str
    problem: str
    decision: str
    reasoning: str
    alternatives: Optional[str] = None
    selected_option: Optional[str] = None
    rejected_options: Optional[str] = None
    risks: Optional[str] = None
    expected_outcome: Optional[str] = None
    actual_outcome: Optional[str] = None
    decision_date: Optional[str] = None
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class IncidentResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    severity: str
    root_cause: Optional[str] = None
    impact: Optional[str] = None
    detection_method: Optional[str] = None
    resolution: Optional[str] = None
    prevention: Optional[str] = None
    incident_date: Optional[str] = None
    expert_involved: Optional[str] = None
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class MeetingResponse(BaseModel):
    id: int
    project_id: int
    title: str
    date: Optional[str] = None
    meeting_type: Optional[str] = None
    participants: Optional[str] = None
    discussion_summary: Optional[str] = None
    decisions_made: Optional[str] = None
    action_items: Optional[str] = None
    outcomes: Optional[str] = None
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class DocumentResponse(BaseModel):
    id: int
    project_id: Optional[int] = None
    title: str
    content: str
    file_type: str
    source_url: Optional[str] = None
    status: str
    extracted_memories_count: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class DocumentExtractRequest(BaseModel):
    title: str
    content: str
    project_id: Optional[int] = None
    expert_id: Optional[int] = None
    file_type: Optional[str] = "TXT"

class DocumentExtractResponse(BaseModel):
    document_id: int
    title: str
    status: str
    extracted_memories: List[DecisionMemoryResponse]
    message: str

class MemoryStatusUpdateRequest(BaseModel):
    status: str  # DRAFT, REVIEW, ACTIVE, REVIEW_REQUIRED, UPDATED, ARCHIVED
    verification_status: Optional[str] = None

class AskRequest(BaseModel):
    query: str
    project_id: Optional[int] = None
    expert_id: Optional[int] = None
    context_hint: Optional[str] = None

class AskResponse(BaseModel):
    query: str
    answer: str
    historical_match_score: str  # High, Medium, Low
    relevant_experiences: List[Dict[str, Any]]
    what_happened: str
    previous_decision: str
    previous_outcome: str
    why_relevant: List[str]
    context_differences: List[str]
    conflicts_detected: List[str]
    assessment: str
    sources: List[str]
    memory_bank_id: str
    decision_memory_id: Optional[int] = None

class FeedbackRequest(BaseModel):
    ask_query: str
    feedback_type: str  # HELPFUL, PARTIALLY_HELPFUL, NOT_HELPFUL
    actual_result: Optional[str] = None
    decision_memory_id: Optional[int] = None

class FeedbackResponse(BaseModel):
    status: str
    message: str
    new_hindsight_memory_id: Optional[str] = None
    updated_decision_memory_id: Optional[int] = None

class KnowledgeHandoffRequest(BaseModel):
    expert_id: int
    project_id: int
    deep_systems: str
    recurring_problems: str
    critical_decisions: str
    sop_exceptions: str
    vital_warnings: str
    past_failures: str
    hidden_dependencies: str
    successor_lessons: str

class KnowledgeHandoffResponse(BaseModel):
    status: str
    expert_id: int
    project_id: int
    created_memories_count: int
    memories: List[DecisionMemoryResponse]

class KnowledgeRiskResponse(BaseModel):
    id: int
    project_id: int
    expert_id: int
    topic: str
    risk_level: str
    criticality: str
    documentation_coverage: float
    verification_level: float
    action_required: str
    expert_name: Optional[str] = None
    project_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class DecisionReplayStep(BaseModel):
    step_number: int
    stage: str  # Problem Detected, Investigation & Options, Decision Made, Action Taken, Realized Outcome, Lessons Learned
    title: str
    description: str
    timestamp: Optional[str] = None
    actor: Optional[str] = None
    status: str = "completed"

class DecisionReplayResponse(BaseModel):
    decision_id: int
    title: str
    project_name: str
    expert_name: str
    decision_date: Optional[str] = None
    steps: List[DecisionReplayStep]

class KnowledgeMapNode(BaseModel):
    id: str
    label: str
    type: str  # project, expert, incident, decision, technology, lesson
    group: Optional[str] = None

class KnowledgeMapEdge(BaseModel):
    source: str
    target: str
    label: str

class KnowledgeMapResponse(BaseModel):
    nodes: List[KnowledgeMapNode]
    edges: List[KnowledgeMapEdge]

class AdminStatusResponse(BaseModel):
    database: Dict[str, Any]
    hindsight: Dict[str, Any]
    llm: Dict[str, Any]
    counts: Dict[str, int]
    system_version: str

class SeedRequest(BaseModel):
    profile: str = "DEV"  # DEV, DEMO, FULL, STRESS

class SeedResponse(BaseModel):
    status: str
    profile: str
    seeded_counts: Dict[str, int]
