from typing import List, Optional, Any
from agno.agent import Agent
from agno.models.mistral import MistralChat

from app.memory import get_shared_db
from app.utils import get_agent_prompt

def create_agent(
    name: str,
    slug: str,
    model_id: str = "mistral-large-latest",
    tools: Optional[List[Any]] = None,
    output_schema: Optional[Any] = None,
    user_id: str = "civic-system",
    reasoning: bool = True,
) -> Agent:
    """
    Factory function to create a standardized Civic Remediation Agent.
    Handles prompt loading (with fallback), memory connection, and model setup.
    """
    # Load prompt
    prompt = get_agent_prompt(slug)
    
    # Create Agent
    return Agent(
        name=name,
        model=MistralChat(id=model_id),
        tools=tools or [],
        output_schema=output_schema,
        reasoning=reasoning,
        db=get_shared_db(),
        update_memory_on_run=True,
        user_id=user_id,
        # We can inject instructions/prompts here if needed, 
        # but the current agents manage prompt formatting themselves in methods.
    )

class BaseAgent:
    """Base class for all civic agents to handle common setup."""
    def __init__(self, name: str, slug: str, user_id: str = "civic-system"):
        self.prompt = get_agent_prompt(slug)
        self.user_id = user_id
