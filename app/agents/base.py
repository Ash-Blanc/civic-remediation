from typing import List, Optional, Any
from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.tools.reasoning import ReasoningTools

from app.memory import get_shared_db
from app.utils import get_agent_prompt

def create_agent(
    name: str,
    slug: str,
    model_id: str = "mistral-large-latest",
    tools: Optional[List[Any]] = None,
    output_schema: Optional[Any] = None,
    user_id: str = "civic-system",
    enable_reasoning_tools: bool = True,
) -> Agent:
    """
    Factory function to create a standardized Civic Remediation Agent.
    Handles prompt loading (with fallback), memory connection, and model setup.
    
    Args:
        enable_reasoning_tools: If True, adds ReasoningTools (think/analyze) that agents
                               can use selectively. If False, no reasoning capabilities.
    """
    # Load prompt and extract system instructions
    prompt = get_agent_prompt(slug)
    
    # Extract system message content for agent instructions
    instructions = None
    try:
        # Format with empty placeholders to get the messages
        messages = prompt.format()
        for msg in messages:
            if msg.role == "system":
                instructions = msg.content
                break
    except Exception:
        # If formatting fails (missing vars), try raw access
        pass
    
    # Build tools list
    agent_tools = tools or []
    if enable_reasoning_tools:
        # Add reasoning tools so agent can choose when to think/analyze
        agent_tools = [ReasoningTools()] + agent_tools
    
    # Create Agent with instructions
    return Agent(
        name=name,
        model=MistralChat(id=model_id),
        instructions=instructions,  # Give agent its specialized identity
        tools=agent_tools,
        output_schema=output_schema,
        db=get_shared_db(),
        update_memory_on_run=True,
        user_id=user_id,
    )

class BaseAgent:
    """Base class for all civic agents to handle common setup."""
    def __init__(self, name: str, slug: str, user_id: str = "civic-system"):
        self.prompt = get_agent_prompt(slug)
        self.user_id = user_id
