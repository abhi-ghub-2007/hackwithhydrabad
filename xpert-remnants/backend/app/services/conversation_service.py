"""
Multi-turn Conversation State & Session Tracking (Antigravity 3.8 Flash)
Tracks:
- Conversation history
- Active project & expert scopes across follow-up turns
- Pending decision change protocol state
- Retrieved historical evidence IDs
"""
from typing import Dict, Any, Optional
import time


class ConversationState:
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.last_query: Optional[str] = None
        self.last_answer: Optional[str] = None
        self.last_project_id: Optional[int] = None
        self.last_project_name: Optional[str] = None
        self.last_expert_id: Optional[int] = None
        self.last_expert_name: Optional[str] = None
        self.last_decision_id: Optional[int] = None
        self.last_decision_text: Optional[str] = None
        self.last_reasoning: Optional[str] = None
        self.last_lessons: Optional[str] = None
        self.last_impact: Optional[str] = None
        self.last_topic: Optional[str] = None
        self.last_candidate_option: Optional[str] = None
        self.last_sources: list = []
        self.last_referenced_experts: list = []
        self.last_saved_reason: Optional[str] = None
        self.pending_decision: Optional[Dict[str, Any]] = None
        self.turn_history: list = []
        self.updated_at: float = time.time()


class ConversationService:
    def __init__(self):
        self._sessions: Dict[str, ConversationState] = {}

    def get_or_create(self, conversation_id: Optional[str]) -> ConversationState:
        cid = conversation_id or "default_session"
        if cid not in self._sessions:
            self._sessions[cid] = ConversationState(cid)
        return self._sessions[cid]

    def set_pending_decision(self, conversation_id: Optional[str], pending_data: Dict[str, Any]):
        session = self.get_or_create(conversation_id)
        session.pending_decision = pending_data
        session.updated_at = time.time()

    def get_pending_decision(self, conversation_id: Optional[str]) -> Optional[Dict[str, Any]]:
        session = self.get_or_create(conversation_id)
        return session.pending_decision

    def clear_pending_decision(self, conversation_id: Optional[str]):
        session = self.get_or_create(conversation_id)
        session.pending_decision = None
        session.updated_at = time.time()

    def update_context(
        self,
        conversation_id: Optional[str],
        query: Optional[str] = None,
        answer: Optional[str] = None,
        project_id: Optional[int] = None,
        project_name: Optional[str] = None,
        expert_id: Optional[int] = None,
        expert_name: Optional[str] = None,
        decision_id: Optional[int] = None,
        decision_text: Optional[str] = None,
        reasoning: Optional[str] = None,
        lessons: Optional[str] = None,
        impact: Optional[str] = None,
        topic: Optional[str] = None,
        candidate_option: Optional[str] = None,
        sources: Optional[list] = None,
        referenced_experts: Optional[list] = None,
        saved_reason: Optional[str] = None
    ):
        session = self.get_or_create(conversation_id)
        if query:
            session.last_query = query
        if answer:
            session.last_answer = answer
        if project_id:
            session.last_project_id = project_id
        if project_name:
            session.last_project_name = project_name
        if expert_id:
            session.last_expert_id = expert_id
        if expert_name:
            session.last_expert_name = expert_name
        if decision_id:
            session.last_decision_id = decision_id
        if decision_text:
            session.last_decision_text = decision_text
        if reasoning:
            session.last_reasoning = reasoning
        if lessons:
            session.last_lessons = lessons
        if impact:
            session.last_impact = impact
        if topic:
            session.last_topic = topic
        if candidate_option:
            session.last_candidate_option = candidate_option
        if sources is not None:
            session.last_sources = sources
        if referenced_experts is not None:
            session.last_referenced_experts = referenced_experts
        if saved_reason is not None:
            session.last_saved_reason = saved_reason

        if query and answer:
            session.turn_history.append({
                "query": query,
                "answer": answer,
                "topic": session.last_topic,
                "project_id": session.last_project_id
            })
            if len(session.turn_history) > 10:
                session.turn_history = session.turn_history[-10:]

        session.updated_at = time.time()

    def is_unrelated_switch(self, conversation_id: Optional[str], new_query: str) -> bool:
        """
        Detects if a new query introduces a completely different subject,
        preventing stale conversation topic bleed.
        """
        session = self.get_or_create(conversation_id)
        if not session.last_topic:
            return False

        lower = new_query.lower()
        topic_keywords = {
            "database": ["database", "supabase", "postgres", "sql", "db", "table", "schema", "storage", "tier"],
            "kafka": ["kafka", "stream", "broker", "topic", "consumer", "producer", "partition", "lag"],
            "pool": ["pool", "connection", "pgbouncer", "saturation", "timeout"],
            "compiler": ["compiler", "typecheck", "syntax", "ast", "parse", "parser", "typescript"],
            "auth": ["auth", "jwt", "token", "oauth", "session", "identity"]
        }

        current_topic = session.last_topic
        # If new query explicitly mentions a completely different topic family
        for family, kws in topic_keywords.items():
            if family != current_topic and any(kw in lower for kw in kws):
                # New query belongs to another family, and doesn't mention current topic
                if not any(curr_kw in lower for curr_kw in topic_keywords.get(current_topic, [])):
                    return True

        return False


conversation_service = ConversationService()
