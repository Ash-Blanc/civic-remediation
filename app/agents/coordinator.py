from app.agents.base import create_agent, BaseAgent
from pydantic import BaseModel, Field
from typing import List

class CoordinationPlan(BaseModel):
    task_force_structure: str = Field(..., description="Proposed Joint Task Force or structure")
    priority_remedies: List[str] = Field(..., description="List of administrative/systemic fixes with priority")
    timeline: str = Field(..., description="Phased timeline for intervention")
    ngo_engagement: str = Field(..., description="Specific role for NGOs/partners")

class CoordinatorAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Coordinator", "coordinator", user_id)
        
        self.agent = create_agent(
            name="Coordinator",
            slug="coordinator",
            output_schema=CoordinationPlan,
            user_id=user_id
        )

    def design_coordination(self, findings_json: str) -> CoordinationPlan:
        messages = self.prompt.format(findings_json=findings_json)
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        response = self.agent.run(formatted_messages)
        return response.content
