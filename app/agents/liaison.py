from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.tools import tool
from pydantic import BaseModel, Field

from app.agents.base import create_agent, BaseAgent
from app.agents.liaison import ProposalDraft
from app.memory import get_shared_db
from .strategist import RankedStrategy

class ProposalDraft(BaseModel):
    vendor_name: str
    proposal_title: str
    email_draft: str
    next_steps: str


@tool(requires_confirmation=True)
def submit_proposal(vendor_name: str, email_draft: str) -> str:
    """
    Submit the proposal to a vendor via email.
    This action requires human approval before execution.
    """
    # In production, this would send an actual email
    return f"Proposal submitted to {vendor_name}. Email content: {email_draft[:100]}..."


class LiaisonAgent(BaseAgent):
    def __init__(self, user_id: str = "civic-system"):
        super().__init__("Liaison", "liaison", user_id)
        
        self.agent = create_agent(
            name="Liaison",
            slug="liaison",
            tools=[submit_proposal],
            output_schema=ProposalDraft,
            user_id=user_id
        )

    def create_proposal(self, strategy: RankedStrategy) -> ProposalDraft:
        top_vendor = strategy.ranked_vendors[0]  # Assuming sorted
        messages = self.prompt.format(
            vendor_json=top_vendor.model_dump_json(),
            strategy_context=strategy.selected_strategy
        )
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]
        response = self.agent.run(formatted_messages)
        return response.content

    def initiate_contact(self, proposal: ProposalDraft) -> bool:
        """
        Legacy method for CLI-based human-in-the-loop.
        For AgentOS, use the submit_proposal tool with HITL instead.
        """
        print(f"\n--- PROPOSAL FOR {proposal.vendor_name} ---")
        print(f"Title: {proposal.proposal_title}")
        print(f"Email:\n{proposal.email_draft}")
        print("------------------------------------------")
        user_input = input("Do you approve sending this proposal? (yes/no): ")
        return user_input.lower().strip() == "yes"
