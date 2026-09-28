# Development Notes & Local Runbook

## 1. Quick Start (Zero-Configuration Out-of-the-Box)

The project runs completely locally with no paid API keys required.

### Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
python -m app.scripts.seed_database
python run.py
```
Backend runs at: `http://localhost:8000`
Interactive API Docs (Swagger): `http://localhost:8000/docs`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173`

---

## 2. Automated Test Execution

Run backend test suite:
```bash
cd backend
python -m pytest
```

Run frontend build verification:
```bash
cd frontend
npm run build
```

---

## 3. Connecting Live Cloud Services

When ready to connect live Hindsight Cloud and LLM provider:
1. Open `backend/.env`
2. Set:
   ```env
   HINDSIGHT_API_KEY=your_hindsight_api_key
   HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
   HINDSIGHT_BANK_ID=xpert-remnants-northstar

   LLM_PROVIDER=groq
   LLM_MODEL=openai/gpt-oss-120b
   LLM_API_KEY=your_groq_api_key

   DATABASE_URL=postgresql://user:password@localhost:5432/xpert_remnants
   ```
3. Restart backend server: `python run.py`
4. Visit `/admin` in the browser to verify all three components show connected in live mode.

---

## 4. Synthetic Data Generation Scale Profiles

Configure via `backend/.env`: `DATASET_PROFILE=DEV` or via the Admin UI at `/admin`:
- **DEV**: 500 memories, 10 projects, 5 experts (instant local startup).
- **DEMO**: 5,000 memories, 30 projects, 15 experts.
- **FULL**: 100,000 memories, 100 projects, 50 experts.
- **STRESS**: 500,000+ memories.
