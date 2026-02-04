"""
Civic Remediation Team - Intelligent Agent Coordination.
The team leader coordinates all agents and delegates tasks intelligently.
"""
from os import getenv
from agno.agent import Agent
from agno.team import Team
from agno.models.openai.like import OpenAILike

from app.knowledge import get_shared_db, get_civic_knowledge
from app.agents.base import POLLINATIONS_BASE_URL, DEFAULT_MODEL
from app.agents.sentinel import SentinelAgent
from app.agents.investigator import InvestigatorAgent
from app.agents.bureaucrat import BureaucratAgent
from app.agents.auditor import AuditorAgent
from app.agents.engineer import EngineerAgent
from app.agents.coordinator import CoordinatorAgent
from app.agents.liaison import LiaisonAgent


def create_civic_team(user_id: str = "civic-system") -> Team:
    """
    Create a coordinated team of specialized civic remediation agents.
    The team uses a 7-agent structure for deep investigation and systemic solution building.
    """
    # Create individual agents
    sentinel = SentinelAgent(user_id).agent
    investigator = InvestigatorAgent(user_id).agent
    bureaucrat = BureaucratAgent(user_id).agent
    auditor = AuditorAgent(user_id).agent
    engineer = EngineerAgent(user_id).agent
    coordinator = CoordinatorAgent(user_id).agent
    liaison = LiaisonAgent(user_id).agent
    
    # Create the team
    team = Team(
        name="Civic Remediation Deep Team",
        model=OpenAILike(
            id=DEFAULT_MODEL,
            base_url=POLLINATIONS_BASE_URL,
            api_key=getenv("POLLINATIONS_API_KEY", "not-provided"),
        ),
        reasoning=False,
        db=get_shared_db(),
        update_memory_on_run=True,
        knowledge=get_civic_knowledge(),
        search_knowledge=True,
        instructions=[
            "You coordinate a team of high-level specialists for civic infrastructure remediation in India.",
            "IMPORTANT: Focus on high-level systemic failures (departments, funds, pipelines), NOT ground-level behavior.",
            "",
            "DELEGATION WORKFLOW:",
            "1. Sentinel: Scout for the 'Viral Signal' (critical regional breakdown).",
            "2. Investigator: Gather deep evidence (RTI data, reports, metrics).",
            "3. Bureaucrat: Map the departmental bottlenecks and coordination gaps.",
            "4. Auditor: Audit the financial flow and budget utilization.",
            "5. Engineer: Match technical solutions to the investigated technical root causes.",
            "6. Coordinator: Architect a high-level coordination plan to fix broken bureaucratic pipelines.",
            "7. Liaison: Mobilize resources (funding, grants) and finalize costs.",
            "",
            "Synthesize these granular findings into a 'Master Remediation Blueprint' that identifies exactly who is failing, why the money is stuck, and how a joint task force can fix the root cause.",
        ],
        members=[sentinel, investigator, bureaucrat, auditor, engineer, coordinator, liaison],
        add_team_history_to_members=True,
        user_id=user_id,
        add_datetime_to_context=True,
        timezone_identifier="Etc/UTC",
    )
    
    return team
