"""
Lightweight database migration script for Decision Evolution fields.
Ensures decision_memories table has the new schema columns.
"""
from sqlalchemy import inspect, text
from app.db.database import engine

def migrate_decision_evolution_schema():
    insp = inspect(engine)
    existing = [c['name'] for c in insp.get_columns('decision_memories')]
    
    new_cols = [
        ('decision_status', "VARCHAR(50) DEFAULT 'ACTIVE'"),
        ('effective_at', 'VARCHAR(50)'),
        ('supersedes_memory_id', 'INTEGER'),
        ('change_reason', 'TEXT'),
        ('changed_by_user_id', 'VARCHAR(100)'),
        ('change_type', 'VARCHAR(50)'),
        ('is_current', 'BOOLEAN DEFAULT 1')
    ]
    
    with engine.connect() as conn:
        for col_name, col_type in new_cols:
            if col_name not in existing:
                conn.execute(text(f"ALTER TABLE decision_memories ADD COLUMN {col_name} {col_type}"))
                conn.commit()
                print(f"Added column {col_name} to decision_memories")
            else:
                print(f"Column {col_name} already exists.")
    print("Schema migration complete.")

if __name__ == "__main__":
    migrate_decision_evolution_schema()
