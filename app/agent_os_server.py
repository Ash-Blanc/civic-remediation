"""
Civic Remediation AgentOS Configuration.
Serves the autonomous agent team via the Agno AgentOS platform.
"""
from agno.os import AgentOS
from agno.tools.parallel import ParallelTools
from dotenv import load_dotenv

# Import the Team Factory and Agent Factory
from app.team import create_civic_team
from app.agents.base import create_agent

load_dotenv()

# Instantiate the full team
civic_team = create_civic_team()

# Instantiate individual agents for granular access (without output_schema for conversational mode)
sentinel = create_agent(name="Sentinel", slug="sentinel", tools=[ParallelTools(enable_search=True)])
analyst = create_agent(name="Analyst", slug="analyst")
engineer = create_agent(name="Engineer", slug="engineer", tools=[ParallelTools(enable_search=True, enable_extract=True)])
strategist = create_agent(name="Strategist", slug="strategist")
liaison = create_agent(name="Liaison", slug="liaison")

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
