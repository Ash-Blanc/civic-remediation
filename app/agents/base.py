from typing import List, Optional, Any
from os import getenv
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.reasoning import ReasoningTools

from app.memory import get_shared_db
from app.utils import get_agent_prompt

# Pollinations.ai OpenAI-compatible endpoint
POLLINATIONS_BASE_URL = "https://gen.pollinations.ai/v1"
# Default model - can be: openai, openai-fast, qwen-coder, mistral, deepseek, grok, claude, nova-fast, etc.
DEFAULT_MODEL = "nova-fast"

def create_agent(
    name: str,
    slug: str,
    model_id: str = DEFAULT_MODEL,
    tools: Optional[List[Any]] = None,
    output_schema: Optional[Any] = None,
    user_id: str = "civic-system",
    enable_reasoning_tools: bool = True,
) -> Agent:
    """
    Factory function to create a standardized Civic Remediation Agent.
    Handles prompt loading (with fallback), memory connection, and model setup.
    
    Uses Pollinations.ai as the LLM provider via OpenAI-compatible API.
    
    Args:
        model_id: Pollinations.ai model name (openai, mistral, deepseek, claude, etc.)
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
    
    # Create Agent with Pollinations.ai
    return Agent(
        name=name,
        model=OpenAILike(
            id=model_id,
            base_url=POLLINATIONS_BASE_URL,
            api_key=getenv("POLLINATIONS_API_KEY", "not-provided"),  # Optional for Pollinations.ai
        ),
        instructions=instructions,  # Give agent its specialized identity
        tools=agent_tools,
        output_schema=output_schema,
        db=get_shared_db(),
        update_memory_on_run=True,
        user_id=user_id,
        # Provide current datetime context to prevent knowledge cutoff hallucinations
        add_datetime_to_context=True,
        timezone_identifier="Etc/UTC",
    )

class BaseAgent:
    """Base class for all civic agents to handle common setup."""
    def __init__(self, name: str, slug: str, user_id: str = "civic-system"):
        self.prompt = get_agent_prompt(slug)
        self.user_id = user_id
