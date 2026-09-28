# INPUTS REQUIRED FOR LIVE INTEGRATIONS

The table below summarizes human-supplied credentials and external services required for live production/cloud integration. 

> **Note:** The application includes intelligent local fallback mock implementations for Hindsight, PostgreSQL (via SQLite/SQLAlchemy local fallback), and LLMs so that local development, testing, and UI verification run seamlessly out of the box without requiring paid keys.

| Input | Required for Cloud/Live? | Why Needed | Where to Provide | Default / Local Fallback |
| :--- | :--- | :--- | :--- | :--- |
| `HINDSIGHT_API_KEY` | YES (for live Hindsight Cloud) | Memory RETAIN/RECALL/REFLECT API calls | `backend/.env` | Mock Hindsight Service Layer |
| `HINDSIGHT_BASE_URL` | YES (for live Hindsight Cloud) | Base URL for Hindsight API server | `backend/.env` | `https://api.hindsight.vectorize.io` |
| `HINDSIGHT_BANK_ID` | YES | Scope memory to organization bank | `backend/.env` | `xpert-remnants-northstar` |
| `DATABASE_URL` | YES (for PostgreSQL) | Structured application database connection | `backend/.env` | `sqlite:///./xpert_remnants.db` |
| `LLM_PROVIDER` | YES | Provider route for LLM synthesis (`groq`, `openai`, `mock`) | `backend/.env` | `groq` (or `mock`) |
| `LLM_MODEL` | YES | Configured LLM model identifier | `backend/.env` | `openai/gpt-oss-120b` |
| `LLM_API_KEY` | YES (for live LLM reasoning) | API key for LLM provider (Groq, OpenAI, etc.) | `backend/.env` | Local heuristic engine / Mock fallback |
| `FRONTEND_URL` | NO | CORS allowed origin for frontend client | `backend/.env` | `http://localhost:5173` |

---

## How to enable live keys:
1. Open `backend/.env`
2. Update the values for `HINDSIGHT_API_KEY`, `LLM_API_KEY`, and `DATABASE_URL`.
3. Restart backend server (`python run.py`).
