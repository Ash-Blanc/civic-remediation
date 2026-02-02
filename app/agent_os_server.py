"""
Civic Remediation AgentOS Configuration.
Serves the autonomous agent team via the Agno AgentOS platform.
"""
from agno.os import AgentOS
from dotenv import load_dotenv

# Import the Team Factory
from app.team import create_civic_team

# Import Individual Agents (optional, if you want to access them separately in OS)
from app.agents.sentinel import SentinelAgent
from app.agents.analyst import AnalystAgent
from app.agents.engineer import EngineerAgent
from app.agents.strategist import StrategistAgent
from app.agents.liaison import LiaisonAgent

load_dotenv()

# Instantiate the full team
civic_team = create_civic_team()

# Instantiate individual agents for granular access
sentinel = SentinelAgent().agent
analyst = AnalystAgent().agent
engineer = EngineerAgent().agent
strategist = StrategistAgent().agent
liaison = LiaisonAgent().agent

# Create the AgentOS instance
agent_os = AgentOS(
    name="Civic Remediation System",
    description="Autonomous multi-agent system for identifying and remediating civic infrastructure failures.",
    # The primary interface is the coordinated team
    teams=[civic_team],
    # Also expose individual specialists
    agents=[sentinel, analyst, engineer, strategist, liaison],
)

# Get the FastAPI app
app = agent_os.get_app()

if __name__ == "__main__":
    # Serve the application
    # Note: 'app.agent_os_server:app' must match the filename and app variable
    agent_os.serve(app="app.agent_os_server:app", reload=True, port=7777)
