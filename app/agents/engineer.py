from app.agents.base import create_agent, BaseAgent
from agno.tools.parallel import ParallelTools
from pydantic import BaseModel, Field
from typing import List

from app.memory import get_shared_db
from .analyst import RootCauseAnalysis

class Vendor(BaseModel):
    name: str = Field(..., description="Name of the vendor/startup")
    solution: str = Field(..., description="Description of their technical solution")
    website: str = Field(..., description="Website URL if available")
    relevance_score: int = Field(..., description="Relevance to the problem 1-10")

class VendorList(BaseModel):
    vendors: List[Vendor] = Field(..., description="List of potential vendors")

class EngineerAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Engineer", "engineer", user_id)
        
        self.agent = create_agent(
            name="Engineer",
            slug="engineer",
            tools=[ParallelTools(enable_search=True, enable_extract=True)],
            output_schema=VendorList,
            user_id=user_id
        )

    def find_solutions(self, analysis: RootCauseAnalysis) -> VendorList:
        messages = self.prompt.format(root_causes=str(analysis.technical_root_causes))
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        response = self.agent.run(formatted_messages)
        return response.content
