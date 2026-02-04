"""
Knowledge module for Civic Remediation System.
Provides RAG capabilities and shared database configuration.
"""
from app.knowledge.base import get_civic_knowledge, load_documents, persist_agent_findings
from app.knowledge.memory import get_shared_db

__all__ = ["get_civic_knowledge", "load_documents", "get_shared_db", "persist_agent_findings"]
