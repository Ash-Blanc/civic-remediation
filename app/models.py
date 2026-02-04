"""
Singleton Models for Converging Pipeline Architecture.

Each model represents a SINGLE selected item (not a list) that flows
through the pipeline. This enforces the "one thing at a time" principle:
ONE Problem → ONE Cause → ONE Department → ONE Solution → ONE Funding → Launch

Based on the Civic Remediation Pipeline diagram pattern.
"""
from typing import Optional
from pydantic import BaseModel, Field


# =============================================================================
# STAGE 1: Selected Problem
# =============================================================================
class SelectedProblem(BaseModel):
    """
    Stage 1 Output: The ONE most critical civic problem to address.
    The Sentinel agent analyzes multiple problems and selects the single
    most impactful one based on severity and feasibility.
    """
    title: str = Field(..., description="Concise problem title (e.g., 'Polluted Ganga River')")
    location: str = Field(..., description="Precise location (e.g., 'Varanasi-Kanpur stretch')")
    description: str = Field(..., description="2-3 sentence description of the specific failure")
    key_metric: str = Field(..., description="One hard metric (e.g., '12B liters of daily waste')")
    affected_population: str = Field(..., description="Number of people affected")
    severity_score: int = Field(..., ge=1, le=10, description="Impact severity (1-10)")
    feasibility_score: int = Field(..., ge=1, le=10, description="How solvable with intervention (1-10)")
    why_selected: str = Field(..., description="Justification for selecting THIS problem over others")


# =============================================================================
# STAGE 2: Selected Root Cause
# =============================================================================
class SelectedCause(BaseModel):
    """
    Stage 2 Output: The ONE most critical root cause to address.
    The Investigator analyzes multiple factors and selects the single
    most systemic cause - the lever that will have the greatest impact.
    """
    cause_title: str = Field(..., description="Clear title (e.g., 'Industrial Discharge')")
    cause_type: str = Field(..., description="Type: industrial_discharge, municipal_sewage, religious_waste, agricultural_runoff")
    evidence: str = Field(..., description="Key evidence/data supporting this as the root cause")
    contribution_percentage: Optional[str] = Field(None, description="Estimated % contribution to the problem")
    why_critical: str = Field(..., description="Why THIS is the single most important cause to address")


# =============================================================================
# STAGE 3: Selected Department
# =============================================================================  
class SelectedDepartment(BaseModel):
    """
    Stage 3 Output: The ONE department most responsible and capable.
    The Bureaucrat maps departmental responsibilities and selects the
    single most relevant "Active Body" for implementing the solution.
    """
    name: str = Field(..., description="Department/Body name (e.g., 'NMCG - National Mission for Clean Ganga')")
    department_type: str = Field(..., description="Type: govt, private_tech, semi_private_academic")
    jurisdiction: str = Field(..., description="Jurisdiction level (central, state, district)")
    ministry_parent: Optional[str] = Field(None, description="Parent ministry (e.g., 'Jal Shakti Ministry')")
    contact_info: Optional[str] = Field(None, description="Key contact or office location")
    current_initiatives: Optional[str] = Field(None, description="Existing relevant programmes")
    why_responsible: str = Field(..., description="Why THIS department should lead the intervention")


# =============================================================================
# STAGE 4: Selected Solution
# =============================================================================
class SelectedSolution(BaseModel):
    """
    Stage 4 Output: The ONE strategic intervention to implement.
    The Engineer evaluates multiple technical solutions and selects
    the single most effective approach for the identified cause.
    """
    solution_title: str = Field(..., description="Solution name (e.g., 'Decentralized STPs')")
    solution_type: str = Field(..., description="Type: source_treatment, decentralized_stp, river_surface_cleaning, bioremediation")
    technical_approach: str = Field(..., description="Brief technical description of the approach")
    implementation_scale: str = Field(..., description="Pilot/Medium/Large scale")
    estimated_cost_tier: str = Field(..., description="Low (<₹10Cr), Medium (₹10-100Cr), High (>₹100Cr)")
    timeline_estimate: str = Field(..., description="Estimated implementation timeline")
    why_selected: str = Field(..., description="Why THIS solution best addresses the root cause")


# =============================================================================
# STAGE 5: Selected Funding
# =============================================================================
class SelectedFunding(BaseModel):
    """
    Stage 5 Output: The ONE best-matched funding programme.
    The Liaison searches all options and selects the single most
    appropriate funding source for this specific solution.
    """
    programme_name: str = Field(..., description="Funding programme name (e.g., 'World Bank IBRD')")
    funder_type: str = Field(..., description="Type: govt_programme, nonprofit_grant, philanthropist, csr, impact_investor")
    organization: str = Field(..., description="Organization name (e.g., 'World Bank', 'Gates Foundation')")
    amount_available: str = Field(..., description="Available funding amount or range")
    eligibility_match: str = Field(..., description="How this project matches eligibility criteria")
    application_pathway: Optional[str] = Field(None, description="How to apply or engage")
    why_matched: str = Field(..., description="Why THIS funding source is the best fit")


# =============================================================================
# STAGE 6: Final Converged Blueprint
# =============================================================================
class RemediationBlueprint(BaseModel):
    """
    Final Output: The complete converged remediation plan.
    Combines all singleton selections into a cohesive project launch plan.
    
    This is the "Project Launch" output from the pipeline diagram.
    """
    # Converged selections from each stage
    problem: SelectedProblem
    cause: SelectedCause
    department: SelectedDepartment
    solution: SelectedSolution
    funding: SelectedFunding
    
    # Synthesis fields
    project_title: str = Field(..., description="Compelling project title")
    executive_summary: str = Field(..., description="3-5 sentence executive summary")
    total_budget_estimate: str = Field(..., description="Total estimated budget in ₹ Crores")
    pilot_phase_scope: str = Field(..., description="Scope for initial pilot phase (₹X Crores)")
    key_stakeholders: str = Field(..., description="Primary stakeholders to engage")
    next_steps: str = Field(..., description="Immediate next steps for project launch")


# =============================================================================
# Pipeline Context (passed between stages)
# =============================================================================
class PipelineContext(BaseModel):
    """
    Context object passed between pipeline stages.
    Each stage adds its singleton selection to this context.
    """
    original_query: str = Field(..., description="The user's original query/request")
    problem: Optional[SelectedProblem] = None
    cause: Optional[SelectedCause] = None
    department: Optional[SelectedDepartment] = None
    solution: Optional[SelectedSolution] = None
    funding: Optional[SelectedFunding] = None


__all__ = [
    'SelectedProblem',
    'SelectedCause', 
    'SelectedDepartment',
    'SelectedSolution',
    'SelectedFunding',
    'RemediationBlueprint',
    'PipelineContext',
]
