from app.agents.base import create_agent, BaseAgent
from pydantic import BaseModel, Field
from typing import List

from app.memory import get_shared_db
from app.knowledge import get_civic_knowledge
from .sentinel import Pitfall

class RootCauseAnalysis(BaseModel):
    pitfall_title: str = Field(..., description="Title of the pitfall")
    technical_root_causes: List[str] = Field(..., description="List of technical root causes indentified")
    scientific_context: str = Field(..., description="Scientific context backing the analysis")
    severity_score: int = Field(..., description="Severity score from 1-10")

class AnalystAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Analyst", "analyst", user_id)
        
        self.agent = create_agent(
            name="Analyst",
            slug="analyst",
            output_schema=RootCauseAnalysis,
            user_id=user_id
        )

    def analyze_pitfall(self, pitfall: Pitfall) -> RootCauseAnalysis:
        messages = self.prompt.format(pitfall_json=pitfall.model_dump_json())
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        response = self.agent.run(formatted_messages)
        return response.content
