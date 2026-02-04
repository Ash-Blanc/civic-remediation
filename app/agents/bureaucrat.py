from app.agents.base import create_agent, BaseAgent
from pydantic import BaseModel, Field
from typing import List

class BureaucraticMap(BaseModel):
    responsible_departments: List[str] = Field(..., description="List of departments/agencies involved")
    bottlenecks: List[str] = Field(..., description="Specific process/departmental bottlenecks identified")
    jurisdictional_frictions: str = Field(..., description="Description of 'turf wars' or overlap issues")
    key_contacts: str = Field(..., description="Specific offices or types of officials to engage")

class BureaucratAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Bureaucrat", "bureaucrat", user_id)
        
        self.agent = create_agent(
            name="Bureaucrat",
            slug="bureaucrat",
            output_schema=BureaucraticMap,
            user_id=user_id
        )

    def map_bureaucracy(self, investigation_json: str) -> BureaucraticMap:
        messages = self.prompt.format(investigation_json=investigation_json)
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        response = self.agent.run(formatted_messages)
        return response.content
