from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import Base, engine, SessionLocal
from app.models.models import Organization
from app.scripts.seed_database import seed_database
from app.services.hindsight_service import hindsight_service

from app.api import (
    health,
    memories,
    ask,
    experts,
    projects,
    decisions,
    incidents,
    technologies,
    meetings,
    handoff,
    risks,
    admin
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and seed initial demo data if empty
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        org = db.query(Organization).first()
        if not org:
            print("[Startup] Empty database detected. Seeding initial dataset...")
            seed_database(profile_name=settings.DATASET_PROFILE, force=False)
    finally:
        db.close()

    # Initialize Hindsight bank and directives
    try:
        hindsight_service.create_or_get_bank(settings.HINDSIGHT_BANK_ID)
    except Exception as e:
        print(f"[Startup Warning] Could not initialize Hindsight bank: {e}")

    yield
    # Shutdown logic if any

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="XPERT REMNANTS — AI-Powered Organizational Expertise Preservation Platform",
    lifespan=lifespan
)

# CORS configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(health.router, prefix=settings.API_PREFIX, tags=["Health"])
app.include_router(ask.router, prefix=settings.API_PREFIX, tags=["Decision Intelligence (Ask & Feedback)"])
app.include_router(memories.router, prefix=settings.API_PREFIX, tags=["Memories & Extraction"])
app.include_router(decisions.router, prefix=settings.API_PREFIX, tags=["Decisions & Replay"])
app.include_router(experts.router, prefix=settings.API_PREFIX, tags=["Experts & People"])
app.include_router(projects.router, prefix=settings.API_PREFIX, tags=["Projects & Knowledge Map"])
app.include_router(incidents.router, prefix=settings.API_PREFIX, tags=["Incidents"])
app.include_router(technologies.router, prefix=settings.API_PREFIX, tags=["Technologies"])
app.include_router(meetings.router, prefix=settings.API_PREFIX, tags=["Meetings"])
app.include_router(handoff.router, prefix=settings.API_PREFIX, tags=["Knowledge Handoff"])
app.include_router(risks.router, prefix=settings.API_PREFIX, tags=["Knowledge Risks"])
app.include_router(admin.router, prefix=settings.API_PREFIX, tags=["Administration & Diagnostics"])

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "tagline": "Preserve what experience knows.",
        "health": f"{settings.API_PREFIX}/health",
        "docs": "/docs",
        "version": settings.VERSION
    }
