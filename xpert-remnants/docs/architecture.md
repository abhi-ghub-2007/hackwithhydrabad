# XPERT REMNANTS — TARGET ARCHITECTURE SPECIFICATION

```text
                         XPERT REMNANTS
                               │
             ┌─────────────────┴─────────────────┐
             │                                   │
        React Frontend                     FastAPI Backend
             │                                   │
             │                    ┌──────────────┼──────────────┐
             │                    │              │              │
             │                    ▼              ▼              ▼
             │               PostgreSQL     Hindsight       LLM Provider
             │                    │              │              │
             │                    │         RETAIN/RECALL      │
             │                    │           REFLECT         │
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
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              ▼
                       Evidence-Based Answer
                              │
                              ▼
                         User Feedback
                              │
                              ▼
                       Memory Evolution
```

## System Responsibilities

### PostgreSQL
Structured application database: Entities, relationships, permissions, audit logs, raw decision entities, projects, experts, incidents, meetings, knowledge risks.

### Hindsight
Persistent memory layer: Retaining experience memories, observations, recalling historical evidence, reflection and memory evolution.

### LLM Abstraction (`LLMService`)
Configurable LLM provider routing (Groq, OpenAI, or Fallback Engine) for document extraction, memory formatting, and natural language synthesis.
