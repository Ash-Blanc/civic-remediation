"""
Knowledge Base for Civic Remediation System.
Provides RAG capabilities using PgVector.
"""
import os
import json
from datetime import datetime
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.document import Document

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


def persist_agent_findings(findings: dict | list | object, agent_name: str, query: str) -> None:
    """
    Persist agent findings to the knowledge base for future reference.
    
    Args:
        findings: The structured output from an agent (Pydantic model or dict)
        agent_name: Name of the agent that produced the findings
        query: The original query that triggered the findings
    """
    kb = get_civic_knowledge()
    
    # Convert Pydantic model to dict if needed
    if hasattr(findings, 'model_dump'):
        data = findings.model_dump()
    elif hasattr(findings, 'dict'):
        data = findings.dict()
    else:
        data = findings
    
    # Create a searchable text representation
    timestamp = datetime.now().isoformat()
    content = f"""
Agent: {agent_name}
Query: {query}
Timestamp: {timestamp}

Findings:
{json.dumps(data, indent=2, ensure_ascii=False)}
"""
    
    # Create a Document and insert
    doc = Document(
        name=f"{agent_name}_findings_{timestamp[:10]}",
        content=content,
        meta_data={
            "agent": agent_name,
            "query": query,
            "timestamp": timestamp,
            "type": "agent_findings"
        }
    )
    
    kb.load_documents([doc])
    print(f"[KB] Persisted {agent_name} findings for: {query[:50]}...")
