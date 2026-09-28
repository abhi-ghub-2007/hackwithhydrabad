import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL or "sqlite:///./xpert_remnants.db"

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    FastAPI dependency that yields a SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_migrations(target_engine):
    """
    Safely adds missing columns to existing database tables if SQLAlchemy models evolved.
    """
    from sqlalchemy import inspect, text
    inspector = inspect(target_engine)
    existing_tables = inspector.get_table_names()

    with target_engine.connect() as conn:
        for table_name, table in Base.metadata.tables.items():
            if table_name in existing_tables:
                existing_cols = {col["name"] for col in inspector.get_columns(table_name)}
                for col in table.columns:
                    if col.name not in existing_cols:
                        col_type = col.type.compile(target_engine.dialect)
                        default_clause = ""
                        if col.default is not None and hasattr(col.default, 'arg') and not callable(col.default.arg):
                            default_clause = f" DEFAULT '{col.default.arg}'" if isinstance(col.default.arg, str) else f" DEFAULT {col.default.arg}"
                        try:
                            conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col.name} {col_type}{default_clause}"))
                            conn.commit()
                            print(f"[Migration] Added missing column {col.name} ({col_type}) to {table_name}")
                        except Exception as e:
                            print(f"[Migration Warning] Could not add column {col.name} to {table_name}: {e}")

