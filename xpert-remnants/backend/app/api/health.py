from fastapi import APIRouter
from app.schemas import HealthResponse
from app.core.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def get_health():
    """
    Health check endpoint for XPERT REMNANTS API.
    Returns status, environment, and configuration flags.
    """
    return HealthResponse(
        status="ok",
        application=settings.APP_NAME,
        environment=settings.ENVIRONMENT,
        hindsight_configured=settings.is_hindsight_configured,
        llm_configured=settings.is_llm_configured
    )
