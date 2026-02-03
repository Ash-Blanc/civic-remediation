"""
Knowledge Base for Civic Remediation System.
Provides RAG capabilities using PgVector.
"""
import os
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.google import GeminiEmbedder

# Database URL from environment or default
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://ai:ai@localhost:5532/ai"
)

def get_civic_knowledge() -> Knowledge:
    """
    Get the civic infrastructure knowledge base.
    """
    return Knowledge(
        name="Civic Infrastructure Knowledge Base",
        description="Documents about civic infrastructure, remediation techniques, and vendor solutions.",
        vector_db=PgVector(
            table_name="civic_knowledge",
            db_url=DB_URL,
            embedder=GeminiEmbedder(),
        ),
    )


def load_documents(urls: list[str]) -> None:
    """
    Load documents into the knowledge base.
    """
    kb = get_civic_knowledge()
    for url in urls:
        print(f"Loading: {url}")
        kb.insert(url=url)
    print("Knowledge base updated.")
