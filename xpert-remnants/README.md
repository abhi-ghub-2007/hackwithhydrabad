# XPERT REMNANTS

> **Preserve what experience knows.**  
> AI-powered organizational expertise preservation and decision-memory continuity platform.

---

> **Notice:** All enterprise records, scenarios, incidents, and employees in the synthetic development dataset are fictional (Northstar Technologies India). No confidential company data or real individuals are represented.

---

## 1. The Core Problem & Solution

When experienced software architects and engineers leave an organization, companies retain source code and documentation, but lose the **context, reasoning, rejected alternatives, and operational gotchas** behind critical decisions.

Traditional documentation preserves *information*. **XPERT REMNANTS preserves *experience*.**

```text
Problem
   ↓
Context & Telemetry
   ↓
Options Considered & Rejected
   ↓
Decision & Deep Rationale
   ↓
Action Taken
   ↓
Real-World Impact
   ↓
Preserved Lessons & Warnings
   ↓
Future Decision Recall & Outcome Evolution
```

### Core Product Principle
XPERT REMNANTS is **not** an employee clone, a personality simulator, or an autonomous production operator.  
It is **an organizational decision-memory and expertise-continuity system**. It clearly distinguishes historical evidence from current recommendations and never pretends a former employee is speaking.

---

## 2. Architecture Specification

```text
                         XPERT REMNANTS
                               │
             ┌─────────────────┴─────────────────┐
             │                                   │
        React 19 Frontend                  FastAPI Backend
             │                                   │
             │                    ┌──────────────┼──────────────┐
             │                    │              │              │
             │                    ▼              ▼              ▼
             │               PostgreSQL     Hindsight       LLM Provider
             │                    │              │          (Groq / OpenAI)
             │                    │         RETAIN/RECALL       │
             │                    │           REFLECT           │
             │                    │              │              │
             │                    └──────────────┼──────────────┘
             │                                   │
             └───────────────────────────────────┘
                              │
                              ▼
                 Decision Intelligence Layer
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
 Historical Matching   Context Comparison      Outcome Analysis
 (Hindsight RECALL)     (6 Dimensions)       (Conflict Detection)
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              ▼
                    Evidence-Based Answer
                              │
                              ▼
                     Real-World Feedback
                              │
                              ▼
                Hindsight Memory Evolution (RETAIN)
```

### System Responsibilities
1. **PostgreSQL / SQLAlchemy (Structured Source of Truth):**
   Owns entities, relationships, foreign-key integrity, audit trails, knowledge risks, and permission states (`organizations`, `users`, `people`, `experts`, `projects`, `technologies`, `decisions`, `incidents`, `meetings`, `documents`, `decision_memories`, `feedbacks`, `lessons`).
2. **Hindsight (`hindsight-client` Official SDK):**
   Owns persistent memory banks (`xpert-remnants-northstar`), associative multi-strategy recall (semantic + keyword + graph + temporal), memory-bank directives, and continuous learning via `RETAIN`, `RECALL`, and `REFLECT`.
3. **Decision Intelligence Layer:**
   - **Context Comparison Engine:** Identifies *same*, *different*, and *unknown* across service, environment, symptom, trigger, and database headroom.
   - **Conflict Detection Engine:** Flags historical approach contradictions (e.g. DEC-219 connection pool scaling vs DEC-288 PgBouncer pooling under connection ceiling).
   - **Feedback Learning Loop:** Appends empirical post-resolution metrics (e.g. "reduced latency by 54%") into Hindsight memory.

---

## 3. Technology Stack

### Frontend
- **Framework:** React 19 + Vite
- **Routing:** React Router v7
- **Styling:** Vanilla CSS with Design Tokens & Glassmorphism Theme
- **Icons:** Lucide React
- **Client:** Native Fetch API client (`frontend/src/services/api.js`)

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **Server:** Uvicorn
- **Database:** PostgreSQL with local SQLite development fallback
- **ORM:** SQLAlchemy 2.0
- **Validation:** Pydantic v2
- **Memory Engine:** Official Hindsight Python Client (`hindsight-client>=0.10.1`)
- **LLM Abstraction:** `LLMService` (Groq, OpenAI, or Local Heuristic Engine)
- **Testing:** Pytest (17 automated tests)

---

## 4. Platform Pages & Capabilities

| Route | Page | Purpose |
| :--- | :--- | :--- |
| `/` | **Decision Chat** | Memory-grounded decision support with visible expandable evidence drawers, match scores, context differences, and empirical feedback input. |
| `/knowledge` | **Knowledge Library** | Searchable repository of preserved memories, filterable by type, project, expert, and verification status. |
| `/knowledge/capture` | **Capture Memory** | Dual-mode capture: structured manual experience preservation or AI-assisted document ingestion. |
| `/knowledge/review` | **Review Queue** | Human-in-the-loop verification queue where AI-extracted memories in `DRAFT` status must be approved before entering Hindsight. |
| `/knowledge/handoff` | **Expert Handoff** | Guided 8-question institutional interview preserving critical decisions, SOP exceptions, and successor warnings before expert departure. |
| `/projects` | **Projects** | Enterprise system inventory with criticality metrics and domain categorization. |
| `/projects/:id` | **Project Knowledge & Map** | Project overview, associated decisions, knowledge vulnerabilities, and graph node mapping. |
| `/risks` | **Knowledge Risks Engine** | Organizational vulnerability dashboard detecting single-expert dependencies and low documentation coverage. |
| `/decisions/:id` | **Decision Replay** | Chronological 6-stage visual timeline (Problem → Options → Decision → Action → Outcome → Lesson). |
| `/admin` | **Administration & Health** | Live diagnostics of PostgreSQL, Hindsight, and LLM; synthetic scale generator (DEV/DEMO/FULL/STRESS); Hindsight bank synchronization. |

---

## 5. Quick Start & Runbook

### Prerequisites
- Node.js v18+ & npm v9+
- Python 3.10+

### Step 1: Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
python -m app.scripts.seed_database
python run.py
```
*Backend runs on:* `http://localhost:8000`  
*Swagger Documentation:* `http://localhost:8000/docs`

### Step 2: Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Frontend runs on:* `http://localhost:5173`

---

## 6. Environment Configuration

### Backend (`backend/.env`)
```env
ENVIRONMENT=development
PORT=8000
HOST=0.0.0.0

# Structured Database (PostgreSQL URL or SQLite local fallback)
DATABASE_URL=sqlite:///./xpert_remnants.db

# Official Hindsight Python SDK
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=
HINDSIGHT_BANK_ID=xpert-remnants-northstar

# LLM Provider Abstraction
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-120b
LLM_API_KEY=

# Retrieval Configuration
MAX_MEMORY_CONTEXT=4096
MAX_RETRIEVED_MEMORIES=8

# Synthetic Dataset Profile (DEV: 500, DEMO: 5000, FULL: 100000, STRESS: 500000)
DATASET_PROFILE=DEV

# CORS
FRONTEND_URL=http://localhost:5173
```

> **Zero-Key Local Mode:** When `HINDSIGHT_API_KEY` and `LLM_API_KEY` are left blank, XPERT REMNANTS automatically uses local in-memory fallback stores and heuristic reasoning so that local development and automated testing run seamlessly without paid keys.

---

## 7. Synthetic Data Scale Profiles

Configure `DATASET_PROFILE` in `backend/.env` or trigger via the `/admin` UI:
- **DEV**: 500 memories, 10 projects, 5 experts (instant local boot).
- **DEMO**: 5,000 memories, 30 projects, 15 experts.
- **FULL**: 100,000 memories, 100 projects, 50 experts.
- **STRESS**: 500,000+ memories.

---

## 8. Automated Testing

### Backend Test Suite
```bash
cd backend
python -m pytest
```
*Verifies 17 automated tests covering the Ask pipeline, context difference engine, conflict detection, memory lifecycle, document extraction, human review, expert handoff, and Hindsight batch operations.*

### Frontend Production Build
```bash
cd frontend
npm run build
```
*Compiles all 10 platform views and React 19 components with zero errors.*

---

## 9. The Demo Story (1-Minute Judge Walkthrough)

1. **Scene 1 (Departed Expert):** Arjun Mehta, Principal Software Architect, leaves Northstar after 8 years.
2. **Scene 2 (Knowledge Risks):** Visit `/risks`. Observe high-risk vulnerability on Payment Reconciliation with 23 decisions and low documentation coverage.
3. **Scene 3 (Expert Handoff):** Visit `/knowledge/handoff`. Click *"Auto-Fill Arjun Mehta Handoff"* and submit to preserve his deep knowledge into verified Hindsight memory.
4. **Scene 4 (New Problem):** Navigate to `/` (Decision Chat). As a new engineer, ask:
   > *"Payment API latency increased after a traffic spike during sales event. What should I investigate?"*
5. **Scene 5 (Hindsight Recall):** XPERT REMNANTS recalls INC-1842 & DEC-219, explaining:
   - What occurred (connection wait times).
   - What was decided (pool expansion from 50 to 100).
   - What differs today (validating postgres max_connections ceiling).
   - Historical approach conflict with DEC-288.
6. **Scene 6 (Feedback Learning Loop):** In the response, click *"Submit Real-World Outcome"* and enter:
   > *"Increasing the pool reduced latency by 54% in production."*
7. **Scene 7 (Memory Evolution):** The outcome is retained into Hindsight (`xpert-remnants-northstar`). Future queries recall the enriched empirical evidence!
