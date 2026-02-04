from app.agents.base import create_agent, BaseAgent
from agno.tools.parallel import ParallelTools
from pydantic import BaseModel, Field
from typing import List

class FinancialAudit(BaseModel):
    budget_allocated: str = Field(..., description="Amount allocated in official budgets")
    utilization_ratio: str = Field(..., description="Percentage of released funds actually utilized")
    stuck_funds_location: str = Field(..., description="Where the money is currently held/stuck")
    spending_gaps: List[str] = Field(..., description="Identified gaps in financial flow")

class AuditorAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Auditor", "auditor", user_id)
        
        self.agent = create_agent(
            name="Auditor",
            slug="auditor",
            tools=[ParallelTools(enable_search=True)],
            output_schema=FinancialAudit,
            user_id=user_id
        )

    def audit_finances(self, bureaucratic_json: str) -> FinancialAudit:
        messages = self.prompt.format(bureaucratic_json=bureaucratic_json)
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        response = self.agent.run(formatted_messages)
        return response.content
