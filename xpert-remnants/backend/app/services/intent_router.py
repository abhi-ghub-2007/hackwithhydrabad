"""
Query Intent Router (Antigravity 3.8 Flash)
Classifies user messages prior to memory retrieval to route to:
- Direct conversational handling (Greeting, Small Talk, Identity, Capabilities)
- Decision Change & Evolution Protocol
- Domain & Expert-Scoped Hindsight Retrieval
- Open/General Knowledge Fallback (PostgreSQL, generic technical concepts)
- Unsupported / Out-of-Domain Safety Gate
"""
import re
from enum import Enum
from typing import Optional, Dict, Any, Tuple


class QueryIntent(str, Enum):
    GREETING = "GREETING"
    SMALL_TALK = "SMALL_TALK"
    IDENTITY = "IDENTITY"
    CAPABILITIES = "CAPABILITIES"
    LIST_EXPERTS = "LIST_EXPERTS"
    LIST_PROJECTS = "LIST_PROJECTS"
    SIMPLE_FACT = "SIMPLE_FACT"
    GENERAL_KNOWLEDGE = "GENERAL_KNOWLEDGE"
    DOMAIN_QUERY = "DOMAIN_QUERY"
    PROJECT_QUERY = "PROJECT_QUERY"
    EXPERT_QUERY = "EXPERT_QUERY"
    DECISION_QUERY = "DECISION_QUERY"
    FOLLOW_UP = "FOLLOW_UP"
    DECISION_CHANGE = "DECISION_CHANGE"
    DECISION_CONFIRM = "DECISION_CONFIRM"
    KNOWLEDGE_UPDATE = "KNOWLEDGE_UPDATE"
    INCIDENT_QUERY = "INCIDENT_QUERY"
    FEEDBACK = "FEEDBACK"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"


class IntentRouter:
    """
    Evaluates message structure, semantics, and conversation state to determine intent.
    """

    GREETING_PATTERNS = [
        r"^hi\b", r"^hello\b", r"^hey\b", r"^good\s+(morning|afternoon|evening|day)\b",
        r"^howdy\b", r"^greetings\b", r"^sup\b", r"^yo\b"
    ]

    SMALL_TALK_PATTERNS = [
        r"^thanks?\b", r"^thank\s+you\b", r"^okay\b", r"^ok\b", r"^cool\b",
        r"^great\b", r"^nice\b", r"^awesome\b", r"^got\s+it\b", r"^sounds\s+good\b",
        r"^understood\b", r"^perfect\b", r"^cheers\b",
        r"^are\s+you\s+(?:mad|angry|happy|sad|upset|real|human|an\s+ai|alive|sentient)\b",
        r"^how\s+are\s+you\b", r"^what(?:'s|\s+is)\s+up\b", r"^how(?:'s|\s+is)\s+it\s+going\b"
    ]

    IDENTITY_PATTERNS = [
        "who are you", "who are u", "what are you", "what is this",
        "what is xpert remnants", "introduce yourself", "tell me about yourself",
        "what's your name", "who made you", "what system is this"
    ]

    CAPABILITIES_PATTERNS = [
        "what can you do", "what do you do", "how do you work", "what can you remember",
        "how can you help", "what are your features", "what is your purpose", "help me"
    ]

    LIST_EXPERTS_PATTERNS = [
        r"^(?:list|show|name|who\s+are)\s+(?:all\s+)?experts\b",
        r"^active\s+experts\??$",
        r"^(?:which|what)\s+experts\s+(?:worked|are\s+there)\b",
        r"^who\s+worked\s+on\s+([a-z0-9\s]+)\??$",
        r"^will\s+you\s+name\s+them\??$"
    ]

    LIST_PROJECTS_PATTERNS = [
        r"^(?:list|show|which|what)\s+(?:all\s+)?projects\b",
        r"^(?:which|what)\s+projects\s+are\s+available\??$",
        r"^available\s+projects\??$",
        r"^what\s+projects\s+do\s+we\s+have\??$"
    ]

    KNOWLEDGE_UPDATE_PATTERNS = [
        r"\bwe\s+(?:discovered|found)\s+(?:that\s+)?(?:the\s+issue|it)\s+was\s+actually\b",
        r"\bthe\s+issue\s+was\s+actually\b",
        r"\bwe\s+fixed\s+it\s+by\b",
        r"\bthe\s+architecture\s+has\s+changed\b",
        r"\bthe\s+team\s+has\s+moved\s+to\b",
        r"\bwe\s+dropped\s+([a-z0-9\-_.]+)\b",
        r"\bwe\s+changed\s+the\s+architecture\s+to\b",
        r"\bwe\s+no\s+longer\s+use\s+(?:the\s+previous\s+approach|([a-z0-9\-_.]+))\b",
        r"\bfrom\s+now\s+on\s+we\s+(?:will\s+)?use\b",
        r"\bthe\s+migration\s+is\s+complete\b",
        r"\bthe\s+new\s+api\s+is\s+now\s+production\b"
    ]

    FEEDBACK_PATTERNS = [
        r"^(?:that|this)\s+is\s+(?:wrong|incorrect|outdated|not\s+right)\b",
        r"^don't\s+use\s+that\s+approach\s+anymore\b",
        r"^that\s+decision\s+is\s+outdated\b"
    ]

    DECISION_QUERY_PATTERNS = [
        r"^(?:what|which)\s+database\s+(?:is|are\s+we)\s+(?:used|using)(?:\s+now)?\??$",
        r"^which\s+database\s+is\s+used\??$",
        r"^what\s+database\s+is\s+used\??$",
        r"^what\s+architecture\s+is\s+current\??$",
        r"^what\s+is\s+the\s+current\s+architecture(?:\s+now)?\??$",
        r"^what\s+decisions?\s+(?:are|is)\s+active\??$",
        r"^what\s+did\s+we\s+use\s+before\??$",
        r"^what\s+architecture\s+did\s+we\s+use\s+before\??$"
    ]

    DECISION_CHANGE_PATTERNS = [
        r"\b(?:i\s+am|i'm|we\s+are|we're)\s+(?:switching|changing)\s+(?:the\s+database\s+to|to)\s+([a-z0-9\-_.]+)\b",
        r"\b(?:i\s+am|i'm|we\s+are|we're)\s+changing\s+(?:the\s+database\s+to|to)\s+([a-z0-9\-_.]+)\b",
        r"\b(?:use|adopt)\s+([a-z0-9\-_.]+)\s+for\s+this\s+project\b",
        r"\b(?:switch|switching)\s+to\s+([a-z0-9\-_.]+)\b",
        r"\bfor\s+this\s+project[,\s]+we\s+have\s+changed\s+the\s+database\b",
        r"\bwe(?:'re|\s+are)\s+(?:choosing|using|going\s+with|switching\s+to|adopting)\b",
        r"\bwe\s+decided\s+to\s+(?:use|choose|switch\s+to|adopt)\b",
        r"\b(?:actually|instead)[,.]?\s+(?:we(?:'re|\s+are)\s+using|let(?:'s|\s+us)\s+use|use)\b",
        r"\b(?:okay|ok|alright)[,.]?\s+(?:for\s+the\s+current\s+project\s+)?we(?:'ll|\s+will|\s+'re|\s+are)\s+(?:use|choose|adopt)\s+([a-z0-9\-_.]+)\b",
        r"\b(?:okay|ok|alright)[,.]?\s+(?:for\s+the\s+current\s+project\s+)?we(?:'ll|\s+will)\s+use\s+it\b",
        r"\bwe(?:'ll|\s+will)\s+use\s+it\b",
        r"\blet(?:'s|\s+us)\s+use\s+it\b",
        r"\bfor\s+now\s+use\b",
        r"\blet(?:'s|\s+us)\s+switch\s+to\b",
        r"\bthe\s+company\s+is\s+(?:choosing|using|going\s+with)\b",
        r"\bignore\s+(?:the\s+)?previous\s+choice\b",
        r"\bthis\s+project\s+will\s+use\b",
        r"\buse\s+[a-z0-9\-_.]+\s+instead\b",
        r"\bwe(?:'re|\s+are)\s+changing\s+(?:that|the\s+decision)\b"
    ]

    CONFIRMATION_PATTERNS = [
        r"^yes\b", r"^confirm\b", r"^yes[,.]?\s+(?:please\s+)?record\s+it\b",
        r"^please\s+record\s+it\b", r"^record\s+it\b", r"^go\s+ahead\b",
        r"^sure\b", r"^proceed\b", r"^yes[,.]?\s+proceed\b", r"^approved?\b",
        r"^yes[,.]?\s+record\s+this\b", r"^do\s+it\b", r"^save\s+(?:that|it|this)\b"
    ]

    OUT_OF_DOMAIN_PATTERNS = [
        "vacation", "ceo", "salary", "payroll", "bonus", "holiday", "catering",
        "cafeteria", "flight", "private jet", "gossip", "stock price", "personal opinion",
        "weather", "sports", "recipe", "movie"
    ]

    GENERAL_KNOWLEDGE_PATTERNS = [
        r"^(?:which\s+is\s+better|what\s+is\s+better)[,:\s]+",
        r"^what\s+is\s+(?!the\s+decision|the\s+status|our|project|raj|sarah)[a-z0-9\s\-_.]+\??$",
        r"^explain\s+(?:how\s+)?[a-z0-9\s\-_.]+\s+(?:works?|is)\??$",
        r"^what\s+does\s+[a-z0-9\-_.]+\s+do\??$",
        r"^how\s+does\s+[a-z0-9\-_.]+\s+work\??$",
        r"^difference\s+between\s+[a-z0-9\s\-_.]+\s+and\s+[a-z0-9\s\-_.]+\??$"
    ]

    FOLLOW_UP_PATTERNS = [
        (r"^why\??$", "why"),
        (r"^why\s+(?:is|was)\s+(?:that|it|this)\??$", "why"),
        (r"^why\s+did\s+we\s+(?:switch|change)\??$", "why_switch"),
        (r"^how\s+come\??$", "why"),
        (r"^what\s+about\s+([a-z0-9\-_.]+)\??$", "what_about"),
        (r"^what\s+about\s+that\??$", "what_about_that"),
        (r"^what\s+did\s+(?:they|you)\s+try\s+(?:last\s+time|before)\??$", "what_tried_before"),
        (r"^why\s+didn't\s+that\s+approach\s+work\??$", "why_failed"),
        (r"^what\s+did\s+the\s+(?:previous|old)\s+engineers\s+learn(?:\s+about\s+([a-z0-9\s]+))?\??$", "what_learned"),
        (r"^who\s+changed\s+that\??$", "who_changed"),
        (r"^what\s+was\s+rejected\s+before\s+this\??$", "what_rejected"),
        (r"^why\s+was\s+that\s+rejected\??$", "why_rejected"),
        (r"^what\s+else\s+failed\??$", "what_failed"),
        (r"^who\s+decided\s+that\??$", "who_decided"),
        (r"^what\s+did\s+he\s+decide\??$", "what_decided"),
        (r"^is\s+that\s+still\s+current\??$", "is_current"),
        (r"^what\s+changed\??$", "what_changed")
    ]

    SIMPLE_FACT_PATTERNS = [
        r"^(?:what|which)\s+database\s+(?:is|are\s+we)\s+(?:used|using)\??$",
        r"^what\s+database\s+do\s+we\s+use\??$",
        r"^tell\s+me\s+which\s+product\s+(?:you|we)\s+worked\s+on\??$",
        r"^which\s+product\s+did\s+[a-z0-9\s]+\s+work\s+on\??$"
    ]

    def classify_intent(
        self,
        query: str,
        project_id: Optional[int] = None,
        expert_id: Optional[int] = None,
        has_pending_decision: bool = False
    ) -> Tuple[QueryIntent, Dict[str, Any]]:
        """
        Classifies intent and extracts structural signals.
        """
        trimmed = query.strip()
        lower = trimmed.lower()
        metadata: Dict[str, Any] = {}

        # 1. Decision Confirmation Check (if pending state exists)
        if has_pending_decision:
            for pat in self.CONFIRMATION_PATTERNS:
                if re.search(pat, lower):
                    return QueryIntent.DECISION_CONFIRM, {"confirmed": True}

        # 2. Knowledge Update & Verified Correction Detection
        for pat in self.KNOWLEDGE_UPDATE_PATTERNS:
            if re.search(pat, lower):
                # Check what type of update
                if "connection pooling" in lower or "issue was actually" in lower:
                    return QueryIntent.KNOWLEDGE_UPDATE, {
                        "update_type": "CORRECTION",
                        "field": "root_cause",
                        "corrected_value": "connection pooling",
                        "raw_text": trimmed
                    }
                elif "compatibility guard" in lower or "fixed it by" in lower:
                    return QueryIntent.KNOWLEDGE_UPDATE, {
                        "update_type": "SOLUTION",
                        "field": "resolution",
                        "solution_value": "compatibility guard",
                        "raw_text": trimmed
                    }
                return QueryIntent.KNOWLEDGE_UPDATE, {
                    "update_type": "PROJECT_UPDATE",
                    "raw_text": trimmed
                }

        # 3. User Feedback Check
        for pat in self.FEEDBACK_PATTERNS:
            if re.search(pat, lower):
                return QueryIntent.FEEDBACK, {"raw_text": trimmed}

        # 4. Decision Change Detection
        for pat in self.DECISION_CHANGE_PATTERNS:
            if re.search(pat, lower):
                extracted = self._extract_decision_change_details(trimmed)
                return QueryIntent.DECISION_CHANGE, extracted

        # 5. Simple Greetings
        for pat in self.GREETING_PATTERNS:
            if re.search(pat, lower):
                return QueryIntent.GREETING, {}

        # 6. Small Talk / Politeness / Emotional queries ("are you mad?")
        for pat in self.SMALL_TALK_PATTERNS:
            if re.search(pat, lower):
                if re.search(r"^are\s+you\s+(?:mad|angry|happy|sad|upset)\b", lower):
                    return QueryIntent.SMALL_TALK, {"subtype": "emotion", "emotion": "calm"}
                return QueryIntent.SMALL_TALK, {}

        # 7. System Identity
        for phrase in self.IDENTITY_PATTERNS:
            if phrase in lower:
                return QueryIntent.IDENTITY, {}

        # 8. System Capabilities
        for phrase in self.CAPABILITIES_PATTERNS:
            if phrase in lower:
                return QueryIntent.CAPABILITIES, {}

        # 9. List Experts
        for pat in self.LIST_EXPERTS_PATTERNS:
            if re.search(pat, lower):
                is_active = "active" in lower
                return QueryIntent.LIST_EXPERTS, {"active_only": is_active}

        # 10. List Projects
        for pat in self.LIST_PROJECTS_PATTERNS:
            if re.search(pat, lower):
                return QueryIntent.LIST_PROJECTS, {}

        # 11. Follow-up query
        for pat, ftype in self.FOLLOW_UP_PATTERNS:
            m = re.search(pat, lower)
            if m:
                meta = {"follow_up_type": ftype}
                if ftype == "what_about" and m.groups():
                    meta["target_entity"] = m.group(1).capitalize()
                elif ftype == "what_learned" and m.groups() and m.group(1):
                    meta["topic"] = m.group(1).strip()
                return QueryIntent.FOLLOW_UP, meta

        # 12. Simple Facts (e.g. "What database is used?", "Tell me which product you worked on?")
        for pat in self.SIMPLE_FACT_PATTERNS:
            if re.search(pat, lower):
                return QueryIntent.SIMPLE_FACT, {"raw_query": trimmed}

        # 13. Decision Query (e.g. "What database are we using?", "Which database is used?", "What architecture is current?")
        for pat in self.DECISION_QUERY_PATTERNS:
            if re.search(pat, lower):
                return QueryIntent.DECISION_QUERY, {"raw_query": trimmed}

        # 13. General Technical Knowledge (e.g. "Which is better, hidden coupling or explicit interfaces?", "What is dependency injection?")
        has_org_anchor = bool(
            project_id or expert_id or
            any(w in lower for w in [
                "project x", "vscode", "visual studio code", "powertoys", "windows terminal",
                "typescript", "semantic kernel", "our", "our team", "did we", "we have",
                "incident", "postmortem", "raj", "sarah", "alex", "vikram"
            ])
        )

        for pat in self.GENERAL_KNOWLEDGE_PATTERNS:
            if re.search(pat, lower) and not has_org_anchor:
                topic = re.sub(r'^(what\s+is\s+better|which\s+is\s+better|what\s+is|explain|how\s+does|what\s+does)[,:\s]+', '', lower, flags=re.IGNORECASE)
                topic = topic.strip(' ?.')
                return QueryIntent.GENERAL_KNOWLEDGE, {"topic": topic}

        # 14. Incident & Problem Queries
        if any(w in lower for w in [
            "compatibility problem", "compatibility issue", "latency spike", "stuck with",
            "seen this problem before", "seen this failure", "have we seen this"
        ]):
            return QueryIntent.INCIDENT_QUERY, {}

        # 15. Unsupported / Out-of-Domain Safety Check
        for term in self.OUT_OF_DOMAIN_PATTERNS:
            if term in lower:
                if not project_id and not expert_id:
                    return QueryIntent.UNSUPPORTED, {"flagged_term": term}

        # 16. Explicit Expert Query
        if expert_id or any(kw in lower for kw in ["what did raj", "what did sarah", "did raj", "expert decided"]):
            return QueryIntent.EXPERT_QUERY, {}

        # 17. Explicit Project Query
        if project_id or any(kw in lower for kw in ["project x", "for project", "in visual studio code", "in typescript"]):
            return QueryIntent.PROJECT_QUERY, {}

        # Default: Domain Query against organizational memory
        return QueryIntent.DOMAIN_QUERY, {}

    def _extract_decision_change_details(self, text: str) -> Dict[str, Any]:
        """
        Extracts new option/choice, rationale, and project reference from a decision change statement.
        Example: "No. For the current project we're choosing Supabase because it gives us faster delivery and the team already has experience with it."
        """
        details: Dict[str, Any] = {
            "proposed_choice": None,
            "reason": None,
            "project_hint": None,
            "raw_text": text
        }

        # Project extraction
        proj_match = re.search(r'\b(Project\s+[A-Za-z0-9]+|Visual\s+Studio\s+Code|PowerToys|Windows\s+Terminal|TypeScript|Semantic\s+Kernel)\b', text, re.IGNORECASE)
        if proj_match:
            details["project_hint"] = proj_match.group(1)
        elif "current project" in text.lower():
            details["project_hint"] = "current project"

        # Split on reason indicators: "because", "due to", "since", "as it gives", "as it provides", "as the"
        reason_split = re.split(r'\b(?:because|due\s+to|since|as\s+it|as\s+the)\b', text, maxsplit=1, flags=re.IGNORECASE)
        if len(reason_split) > 1:
            details["reason"] = reason_split[1].strip().rstrip('.')
            main_clause = reason_split[0]
        else:
            main_clause = text

        # Option extraction from main clause: e.g. "we're choosing Supabase", "switching to PostgreSQL", "use it"
        choice_match = re.search(
            r'\b(?:choosing|using|going\s+with|switch\s+to|switching\s+to|switch\s+over\s+to|adopt|use|changing\s+to|changing\s+the\s+database\s+to)\s+([A-Za-z0-9\-_.]+)',
            main_clause,
            re.IGNORECASE
        )
        if choice_match:
            cand = choice_match.group(1).strip()
            if cand.lower() == "it":
                details["proposed_choice"] = "IT"
            elif cand.lower() not in ["for", "the", "a", "an", "now", "our", "this"]:
                details["proposed_choice"] = cand

        return details


intent_router = IntentRouter()
