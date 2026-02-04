"""
Shared Database Configuration for Civic Remediation Agents.
All agents connect to the same PostgreSQL database for persistent memory.
"""
import os
from agno.db.postgres import PostgresDb

# Database URL from environment or default
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://ai:ai@localhost:5532/ai"
)

def get_shared_db() -> PostgresDb:
    """
    Get a shared database instance for agents.
    All agents using the same DB will share memories and sessions.
    """
    return PostgresDb(
        db_url=DB_URL,
        memory_table="civic_memories",
    )
