# DEMO NARRATIVE SCRIPT — NORTHSTAR TECHNOLOGIES INDIA

## Enterprise Narrative: Northstar Technologies India

### Scene 1: The Departed Expert
- **Principal Software Architect:** Arjun Mehta (Pune R&D Hub) has left the company after 8 years.
- **Problem:** 23 critical decisions were associated with his expertise, 11 incompletely documented.

### Scene 2: Guided Handoff & Knowledge Ingestion
- Run guided expert handoff (`/knowledge/handoff`).
- Ingest past incident report postmortem (`INC-1842: Payment API Latency Spike`).

### Scene 3: The New Incident
- A new engineer faces: "Payment API latency increased after a traffic surge."
- Ask XPERT REMNANTS: *"Payment API latency increased after traffic surge. What did the previous team do?"*

### Scene 4: Hindsight Recall & Context Comparison
- XPERT REMNANTS recalls `INC-1842` & decision `DEC-219`.
- Shows:
  - **Previous Decision:** Expanded database connection pool from 50 to 100.
  - **Previous Outcome:** Latency reduced by 68%.
  - **Context Difference:** Current DB connection limit is already near max.
  - **Warning:** Arjun noted: *"Do not expand connection pool if max_connections > 300; optimize queries instead."*

### Scene 5: Outcome Feedback & Memory Evolution
- Engineer applies query optimization & pool tuning.
- Engineer submits feedback: *"Latency reduced by 54%."*
- System retains new outcome in Hindsight.
- Subsequent query reflects updated evidence!
