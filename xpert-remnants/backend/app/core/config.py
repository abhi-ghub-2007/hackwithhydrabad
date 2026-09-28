import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "XPERT REMNANTS")
    PROJECT_NAME: str = APP_NAME
    VERSION: str = "0.2.0"
    API_PREFIX: str = "/api"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Structured Database (PostgreSQL with SQLite local dev fallback)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./xpert_remnants.db")

    # Hindsight Memory Engine
    HINDSIGHT_BASE_URL: str = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
    HINDSIGHT_API_KEY: str = os.getenv("HINDSIGHT_API_KEY", "")
    HINDSIGHT_BANK_ID: str = os.getenv("HINDSIGHT_BANK_ID", "xpert-remnants-northstar")

    # LLM Service Abstraction
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")  # groq, openai, mock
    LLM_MODEL: str = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")

    # Retrieval and Memory Limits
    MAX_MEMORY_CONTEXT: int = int(os.getenv("MAX_MEMORY_CONTEXT", "4096"))
    MAX_RETRIEVED_MEMORIES: int = int(os.getenv("MAX_RETRIEVED_MEMORIES", "8"))

    # Synthetic Dataset Profile: DEV (500), DEMO (5000), FULL (100000), STRESS (500000)
    DATASET_PROFILE: str = os.getenv("DATASET_PROFILE", "DEV")

    @property
    def is_hindsight_configured(self) -> bool:
        return bool(self.HINDSIGHT_API_KEY.strip())

    @property
    def is_llm_configured(self) -> bool:
        return bool(self.LLM_API_KEY.strip())

settings = Settings()
