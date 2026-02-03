"""
Civic Remediation Team - Intelligent Agent Coordination.
The team leader coordinates all agents and delegates tasks intelligently.
"""
from os import getenv
from agno.agent import Agent
from agno.team import Team
from agno.models.openai.like import OpenAILike

from app.memory import get_shared_db
from app.agents.base import POLLINATIONS_BASE_URL, DEFAULT_MODEL
from app.knowledge import get_civic_knowledge
from app.agents.sentinel import SentinelAgent, Pitfall
from app.agents.analyst import AnalystAgent, RootCauseAnalysis
from app.agents.engineer import EngineerAgent, VendorList
from app.agents.strategist import StrategistAgent, RankedStrategy
from app.agents.liaison import LiaisonAgent, ProposalDraft


def create_civic_team(user_id: str = "civic-system") -> Team:
    """
    Create a coordinated team of civic remediation agents.
    The team leader intelligently delegates tasks and synthesizes results.
    """
    # Create individual agents
    sentinel = SentinelAgent(user_id).agent
    analyst = AnalystAgent(user_id).agent
    engineer = EngineerAgent(user_id).agent
    strategist = StrategistAgent(user_id).agent
    liaison = LiaisonAgent(user_id).agent
    
    # Create the team
    # In Agno, the Team object acts as the leader/coordinator
    # Create the team
    # In Agno, the Team object acts as the leader/coordinator
    team = Team(
        name="Civic Remediation Team",
        model=OpenAILike(
            id=DEFAULT_MODEL,
            base_url=POLLINATIONS_BASE_URL,
            api_key=getenv("POLLINATIONS_API_KEY", "not-provided"),
        ),
        reasoning=False,  # Disable verbose reasoning output for clean end-user responses
        db=get_shared_db(),
        update_memory_on_run=True,
        knowledge=get_civic_knowledge(),
        search_knowledge=True,
        instructions=[
            "You coordinate a team of specialists for civic infrastructure remediation.",
            "Delegate tasks to the appropriate team member based on their expertise:",
            "- Sentinel: Identifies systemic failures and pitfalls",
            "- Analyst: Performs root cause analysis",
            "- Engineer: Finds vendor solutions",
            "- Strategist: Ranks solutions using MCDM",
            "- Liaison: Drafts partnership proposals",
            "Synthesize results from all agents into a comprehensive response.",
        ],
        members=[sentinel, analyst, engineer, strategist, liaison],
        add_team_history_to_members=True,  # Shared context
        user_id=user_id,
        # Provide current datetime context to prevent knowledge cutoff hallucinations
        add_datetime_to_context=True,
        timezone_identifier="Etc/UTC",
    )
    
    return team
