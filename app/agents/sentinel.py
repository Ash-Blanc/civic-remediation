from app.agents.base import create_agent, BaseAgent
from agno.tools.parallel import ParallelTools
from pydantic import BaseModel, Field
from typing import List

from app.knowledge import get_civic_knowledge, persist_agent_findings
from app.models import SelectedProblem


# Legacy schema - kept for backward compatibility
class CivicProblem(BaseModel):
    """A specific, actionable civic problem identified in a region."""
    problem_title: str = Field(..., description="Concise title (e.g., 'Patna Ring Road Land Acquisition Stalled')")
    exact_location: str = Field(..., description="Precise location (district, city, ward, or specific site)")
    problem_description: str = Field(..., description="2-3 sentence description of the specific failure")
    affected_population: str = Field(..., description="Number or estimate of people affected")
    key_metric: str = Field(..., description="One hard metric (e.g., '₹450 Cr stuck', '12 km incomplete', '3 year delay')")
    source_url: str = Field(..., description="URL of news/report source")
    severity_score: int = Field(..., ge=1, le=10, description="1-10 score: impact severity")
    feasibility_score: int = Field(..., ge=1, le=10, description="1-10 score: how solvable with intervention")
    estimated_cost_tier: str = Field(..., description="Low (<₹10Cr), Medium (₹10-100Cr), High (>₹100Cr)")


class RankedCivicProblems(BaseModel):
    """Legacy: Ranked list of specific civic problems for a region."""
    region: str = Field(..., description="The region/state being analyzed")
    problems: List[CivicProblem] = Field(..., description="List of problems sorted by priority (severity * feasibility)")


class SentinelAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system", singleton_mode: bool = True):
        super().__init__("Sentinel", "sentinel", user_id)
        
        # Use singleton or list output based on mode
        output_schema = SelectedProblem if singleton_mode else RankedCivicProblems
        
        self.agent = create_agent(
            name="Sentinel",
            slug="sentinel",
            tools=[ParallelTools(enable_search=True)],
            output_schema=output_schema,
            user_id=user_id
        )
        self.singleton_mode = singleton_mode

    def search_for_problems(self, query: str, persist_to_kb: bool = True) -> SelectedProblem:
        """
        Search for civic problems and SELECT the ONE most critical.
        
        Args:
            query: The region or topic to scan (e.g., "Bihar infrastructure")
            persist_to_kb: If True, automatically save findings to KB for other agents
        """
        messages = self.prompt.format(query=query)
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        
        response = self.agent.run(formatted_messages)
        result = response.content
        
        # Auto-persist to KB so other agents can reference these findings
        if persist_to_kb and result:
            try:
                persist_agent_findings(result, "Sentinel", query)
            except Exception as e:
                print(f"[KB] Warning: Failed to persist findings: {e}")
        
        return result

