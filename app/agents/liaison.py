from typing import List, Optional
from agno.agent import Agent
from agno.tools import tool
from agno.tools.parallel import ParallelTools
from pydantic import BaseModel, Field

from app.agents.base import create_agent, BaseAgent


class FundingSource(BaseModel):
    """A potential funding source for civic remediation."""
    name: str = Field(..., description="Name of the funding source (organization, grant, philanthropist)")
    source_type: str = Field(..., description="Type: nonprofit, government_grant, philanthropist, crowdfunding, corporate_csr, foundation")
    description: str = Field(..., description="Brief description of the funding opportunity")
    estimated_amount: Optional[str] = Field(None, description="Potential funding amount or range")
    application_url: Optional[str] = Field(None, description="URL to apply or learn more")
    eligibility_notes: str = Field(..., description="Key eligibility requirements or notes")


class CostEstimate(BaseModel):
    """Cost breakdown for a civic remediation project."""
    category: str = Field(..., description="Cost category (e.g., materials, labor, permits, equipment)")
    description: str = Field(..., description="Description of the cost item")
    estimated_cost: float = Field(..., description="Estimated cost in USD")
    notes: Optional[str] = Field(None, description="Additional notes or assumptions")


class FundingPlan(BaseModel):
    """Complete funding plan for civic remediation."""
    project_summary: str = Field(..., description="Summary of the remediation project being funded")
    total_estimated_cost: float = Field(..., description="Total estimated cost for the project in USD")
    cost_breakdown: List[CostEstimate] = Field(..., description="Detailed breakdown of costs")
    funding_sources: List[FundingSource] = Field(..., description="Identified funding opportunities")
    funding_gap: float = Field(..., description="Gap between identified funding and total cost")
    recommendations: str = Field(..., description="Strategic recommendations for securing funding")
    timeline_estimate: str = Field(..., description="Estimated timeline for funding acquisition")


@tool
def search_nonprofit_grants(topic: str, location: str = "") -> str:
    """
    Search for nonprofit grants and funding opportunities related to civic infrastructure.
    
    Args:
        topic: The civic remediation topic (e.g., "water infrastructure", "road repair", "public transit")
        location: Optional geographic focus (e.g., "California", "United States")
    """
    search_query = f"nonprofit grants funding {topic} civic infrastructure {location}".strip()
    # Uses DuckDuckGo via the agent's built-in tools
    return f"Searching for grants: {search_query}"


@tool
def search_philanthropic_foundations(focus_area: str) -> str:
    """
    Search for philanthropic foundations that fund civic and infrastructure projects.
    
    Args:
        focus_area: The focus area (e.g., "urban development", "environmental remediation", "community infrastructure")
    """
    return f"Searching philanthropic foundations for: {focus_area}"


@tool
def search_government_programs(program_type: str, jurisdiction: str = "federal") -> str:
    """
    Search for government funding programs for infrastructure.
    
    Args:
        program_type: Type of program (e.g., "infrastructure grants", "community development", "environmental cleanup")
        jurisdiction: federal, state, or local
    """
    return f"Searching {jurisdiction} government programs for: {program_type}"


@tool
def estimate_project_cost(
    project_type: str,
    scope_description: str,
    scale: str = "medium"
) -> str:
    """
    Generate a cost estimate for a civic remediation project.
    
    Args:
        project_type: Type of project (e.g., "road repair", "water main replacement", "bridge restoration")
        scope_description: Description of the project scope and requirements
        scale: small, medium, or large scale project
    """
    return f"Estimating costs for {scale} scale {project_type}: {scope_description}"


class LiaisonAgent(BaseAgent):
    """
    Funding Coordinator Agent - Finds funding opportunities and estimates costs
    for civic remediation projects. Uses Parallel Tools for comprehensive research.
    
    Searches for:
    - Non-profit grants
    - Philanthropic foundations
    - Government programs
    - Corporate CSR initiatives
    - Crowdfunding opportunities
    """
    
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Liaison", "liaison", user_id)
        
        self.agent = create_agent(
            name="Liaison",
            slug="liaison",
            tools=[
                # ParallelTools for comprehensive web research on funding opportunities
                ParallelTools(enable_search=True, enable_extract=True),
                search_nonprofit_grants,
                search_philanthropic_foundations,
                search_government_programs,
                estimate_project_cost,
            ],
            output_schema=FundingPlan,
            user_id=user_id
        )

    def create_funding_plan(self, project_description: str, location: str = "") -> FundingPlan:
        """
        Create a comprehensive funding plan for a civic remediation project.
        
        Args:
            project_description: Description of the remediation project
            location: Geographic location for targeted funding search
        """
        prompt = f"""
        Create a comprehensive funding plan for this civic remediation project:
        
        Project: {project_description}
        Location: {location or "Not specified"}
        
        Please:
        1. Estimate the total project cost with detailed breakdown
        2. Search for and identify ALL possible funding sources including:
           - Non-profit grants
           - Philanthropic foundations and philanthropists
           - Government grants (federal, state, local)
           - Corporate CSR programs
           - Crowdfunding platforms
           - Community development financial institutions (CDFIs)
           - Impact investors
        3. Calculate any funding gap
        4. Provide strategic recommendations for securing the funding
        5. Estimate a realistic timeline for funding acquisition
        """
        response = self.agent.run(prompt)
        return response.content

    # Keep legacy method for backward compatibility
    def create_proposal(self, strategy) -> FundingPlan:
        """Legacy method - now creates a funding plan instead of vendor proposal."""
        project_desc = getattr(strategy, 'selected_strategy', str(strategy))
        return self.create_funding_plan(project_desc)


# Export the new schema for use elsewhere
__all__ = ['LiaisonAgent', 'FundingPlan', 'FundingSource', 'CostEstimate']
