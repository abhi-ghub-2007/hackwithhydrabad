# HINDSIGHT ARCHITECTURE & INTEGRATION SPECIFICATION

> **XPERT REMNANTS — Persistent Organizational Memory Engine**

---

## 1. Why Hindsight?
XPERT REMNANTS uses **Hindsight** as the persistent memory system for organizational expertise retention.
Unlike document search or static vector databases, Hindsight provides:
- **RETAIN**: Continuous knowledge capture with context preservation.
- **RECALL**: Evidence-grounded retrieval matching historical problems to past decisions and outcomes.
- **REFLECT**: Deep contextual reasoning over accumulated memory banks.

---

## 2. Memory Bank Scope
- **Main Bank ID**: `xpert-remnants-northstar` (configurable via `HINDSIGHT_BANK_ID`).
- **Bank Mission**:
  > You are an organizational expertise continuity agent. Your purpose is to preserve and reason over historical organizational experiences, decisions, reasoning, outcomes, warnings, and lessons. Use historical evidence to help employees understand how similar situations were previously handled. Never treat historical decisions as automatically correct. Detect context differences, conflicting decisions, and uncertainty. Never impersonate or speak as a former employee.

---

## 3. Directives & Rules
1. **Evidence vs Recommendation**: Clearly separate what historical memory contains from what is recommended today.
2. **Factuality**: Do not fabricate historical events or attributes.
3. **Context Comparison**: Always compare current technical stack, environment, and traffic parameters with past incidents.
4. **Conflict Detection**: Explicitly surface when two past decisions led to contradicting outcomes.
5. **No Credentials**: Secret screening strips tokens/passwords prior to `RETAIN`.

---

## 4. Operational API Flow

```text
User Query
    ↓
GET /api/ask
    ↓
Hindsight RECALL (Bank: xpert-remnants-northstar)
    ↓
Context Difference Engine (PostgreSQL vs Current Query)
    ↓
Hindsight REFLECT / LLM Reasoning
    ↓
Evidence-Based Response
    ↓
User Feedback (POST /api/ask/feedback)
    ↓
Hindsight RETAIN (New Verified Outcome)
```
