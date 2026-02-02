from app.agents.base import create_agent, BaseAgent
from agno.tools.parallel import ParallelTools
from pydantic import BaseModel, Field

from app.memory import get_shared_db
from app.knowledge import get_civic_knowledge

class Pitfall(BaseModel):
    title: str = Field(..., description="Title of the systemic failure")
    description: str = Field(..., description="Detailed description of the issue")
    metrics: str = Field(..., description="Hard metrics describing the scale (e.g., '12B liters waste')")
    source_url: str = Field(..., description="URL of the source news/report")

class SentinelAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Sentinel", "sentinel", user_id)
        
        self.agent = create_agent(
            name="Sentinel",
            slug="sentinel",
            tools=[ParallelTools(enable_search=True)],
            output_schema=Pitfall,
            user_id=user_id
        )

    def search_for_pitfalls(self, query: str) -> Pitfall:
        messages = self.prompt.format(query=query)
        # Convert to list of dicts for Agno
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        
        response = self.agent.run(formatted_messages)
        return response.content
