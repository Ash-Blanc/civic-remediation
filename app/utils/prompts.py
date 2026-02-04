import yaml
import os
import langwatch.prompts
from typing import List, Dict, Any

class LocalPrompt:
    """Fallback class for local prompts when LangWatch sync fails."""
    def __init__(self, slug: str, messages: List[Dict[str, Any]]):
        self.slug = slug
        self.messages = messages

    def format(self, **kwargs) -> List[Any]:
        """Simple format implementation replacing {{ key }} with value."""
        formatted_messages = []
        for msg in self.messages:
            content = msg.get("content", "")
            role = msg.get("role")
            
            # Simple Jinja2-style replacement
            for key, value in kwargs.items():
                if isinstance(value, str):
                   content = content.replace(f"{{{{ {key} }}}}", value)
                   content = content.replace(f"{{{{{key}}}}}", value)
            
            # Create a simple object that mimics what Agno expects (usually an object with role/content attributes)
            # Or Agno expects a dict? SentinelAgent converts to dict:
            # formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
            # So the object returned by format() must have .role and .content attributes.
            
            class MessageObj:
                def __init__(self, r, c):
                    self.role = r
                    self.content = c
            
            formatted_messages.append(MessageObj(role, content))
            
        return formatted_messages

def get_agent_prompt(slug: str):
    """
    Get prompt from LangWatch, or fallback to local YAML if not found/synced.
    """
    try:
        # Try fetching from LangWatch (requires successful sync)
        return langwatch.prompts.get(slug)
    except (ValueError, Exception) as e:
        print(f"Warning: Could not load prompt '{slug}' from LangWatch ({e}). Falling back to local YAML.")
        
        # Fallback: Read local YAML directly
        yaml_path = os.path.join("prompts", f"{slug}.yaml")
        if os.path.exists(yaml_path):
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f)
                return LocalPrompt(slug, data.get("messages", []))
        
        raise RuntimeError(f"Prompt '{slug}' not found locally or in LangWatch.")
