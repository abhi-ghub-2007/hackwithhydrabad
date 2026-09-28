# hackwithhydrabad

## XPERT REMNANTS — AI-Powered Organizational Knowledge Preservation Platform

XPERT REMNANTS preserves the critical institutional knowledge, architectural reasoning, trade-offs, and failure lessons that departing senior engineers and architects leave behind.

### Quick Start

#### Backend Setup
```bash
cd xpert-remnants/backend
pip install -r requirements.txt
python run.py
```

#### Frontend Setup
```bash
cd xpert-remnants/frontend
npm install
npm run dev
```

### Architecture
- **Backend:** FastAPI, SQLAlchemy, SQLite/PostgreSQL, Official Hindsight SDK integration with zero-key local fallback.
- **Frontend:** React 19, Vite, ChatGPT-style minimal clean AI conversation interface with light/dark mode and expert selection.
