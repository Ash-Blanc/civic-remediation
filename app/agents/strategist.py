from app.agents.base import create_agent, BaseAgent
from pydantic import BaseModel, Field
from typing import List

from app.memory import get_shared_db
from .engineer import VendorList, Vendor

class RankedVendor(BaseModel):
    vendor_name: str
    rank: int
    score: float
    reasoning: str

class RankedStrategy(BaseModel):
    ranked_vendors: List[RankedVendor]
    selected_strategy: str

class StrategistAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Strategist", "strategist", user_id)
        
        self.agent = create_agent(
            name="Strategist",
            slug="strategist",
            output_schema=RankedStrategy,
            user_id=user_id
        )

    def develop_strategy(self, vendors: VendorList) -> RankedStrategy:
        messages = self.prompt.format(vendors_json=vendors.model_dump_json())
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        response = self.agent.run(formatted_messages)
        return response.content
