# Technical Decisions & Architectural Rationale

This document records the architectural and technology choices made in XPERT REMNANTS.

---

## 1. Dual-Store Responsibility: PostgreSQL + Hindsight

### Decision
PostgreSQL is the source of truth for structured enterprise entities, relationships, permissions, audit logs, and foreign key integrity.
Hindsight is the organizational memory engine owning continuous retention, temporal and graph-aware recall, and reflective synthesis.

### Rationale
- Relational state (users, projects, roles, foreign keys) requires ACID guarantees, indexing, and strict schema validation.
- Knowledge and decision memory requires associative recall, temporal relevance, multi-strategy ranking, and continuous memory evolution without schema migrations.
- Keeping these responsibilities separated prevents polluting the relational schema with unstructured memory representations.

---

## 2. Official Hindsight Python SDK with Zero-Credential Dev Mode

### Decision
Use `hindsight-client` (v0.10.1) as the official SDK client, wrapped inside `app.services.hindsight_service.HindsightService`. When `HINDSIGHT_API_KEY` is not provided (e.g. offline local development or unit testing), the service seamlessly activates an in-memory heuristic fallback store preserving the exact same method signatures (`create_or_get_bank`, `retain_memory`, `retain_batch`, `recall_memories`, `reflect`).

### Rationale
- Hackathon requirement mandates official Hindsight technology rather than ad-hoc HTTP wrappers.
- Developers and judges without paid API keys can test and evaluate the complete end-to-end user experience and test suite immediately without friction.

---

## 3. Human-in-the-Loop Memory Lifecycle

### Decision
AI-extracted memories from technical documents (postmortems, ADRs, runbooks) are created in `DRAFT` status and must be explicitly approved by an engineering lead before transitioning to `ACTIVE` and retaining into Hindsight.

### Rationale
- Never allow AI-generated or extracted memories to automatically become trusted organizational memory without verification.
- Enforces Section 23 & 37 requirements.

---

## 4. Multi-Dimensional Context Comparison Engine

### Decision
Implement `ContextComparisonService` comparing 6 operational dimensions: service domain, deployment environment, operational symptom, load trigger, infrastructure technology, and capacity constraints.

### Rationale
- A semantic vector match alone does not imply a past decision is applicable today.
- Surfacing material differences (e.g., database max_connections headroom) prevents catastrophic misapplication of past decisions.

---

## 5. Explicit Conflict Detection

### Decision
When historical decisions took opposing approaches (e.g., DEC-219 pool expansion vs DEC-288 PgBouncer transaction pooling), `ConflictDetectionService` surfaces the conflict explicitly rather than silently selecting one.

### Rationale
- Organizational memory often contains conflicting advice across different system scales or years.
- Explicitly acknowledging historical conflicts builds trust and teaches successors why different approaches worked under different conditions.

---

## 6. Feedback-Driven Memory Evolution

### Decision
`POST /api/ask/feedback` attaches empirical outcomes (e.g. "increasing pool reduced latency by 54%") to the decision and retains new evidence into Hindsight.

### Rationale
- Demonstrates the central value proposition: organizational memory becomes smarter and more accurate through active usage.
