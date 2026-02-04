from app.agents.base import create_agent, BaseAgent
from agno.tools.parallel import ParallelTools
from pydantic import BaseModel, Field
from typing import List, Optional

class Evidence(BaseModel):
    title: str = Field(..., description="Title of the evidence found")
    metrics: str = Field(..., description="Hard metrics identified (e.g., '50% deficit', '10 tons/day')")
    source_links: List[str] = Field(..., description="List of official links/reports found")
    severity_rank: int = Field(..., description="Severity score from 1-10 based on evidence")
    scientific_context: Optional[str] = Field(None, description="Technical/scientific context for the failure")

class InvestigatorAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Investigator", "investigator", user_id)
        
        self.agent = create_agent(
            name="Investigator",
            slug="investigator",
            tools=[ParallelTools(enable_search=True, enable_extract=True)],
            output_schema=Evidence,
            user_id=user_id
        )

    def investigate_signal(self, signal_json: str) -> Evidence:
        messages = self.prompt.format(signal_json=signal_json)
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        response = self.agent.run(formatted_messages)
        return response.content
