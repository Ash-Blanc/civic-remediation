"""
Singleton Pipeline Workflow - Converging Civic Remediation.

Implements the "one thing at a time" principle:
Problem → Cause → Department → Solution → Funding → Project Launch

Each stage receives the previous output and MUST select exactly ONE item,
creating a converging flow toward a cohesive remediation blueprint.
"""
from typing import Optional
from agno.workflow import Workflow, Step, StepInput, StepOutput

from app.models import (
    SelectedProblem,
    SelectedCause,
    SelectedDepartment,
    SelectedSolution,
    SelectedFunding,
    RemediationBlueprint,
    PipelineContext,
)
from app.agents.base import create_agent, POLLINATIONS_BASE_URL, DEFAULT_MODEL
from app.knowledge import get_shared_db


# =============================================================================
# Stage 1: Problem Selection
# =============================================================================
def create_problem_selector() -> Step:
    """Create the problem selection stage."""
    agent = create_agent(
        name="Problem Selector",
        slug="sentinel",
        output_schema=SelectedProblem,
        enable_reasoning_tools=False,  # Disabled - Pollinations models misformat
    )
    
    return Step(
        name="1. Select ONE Problem",
        agent=agent,
        description="Analyze civic problems and SELECT the SINGLE most critical one to address.",
    )


# =============================================================================
# Stage 2: Cause Identification
# =============================================================================
def create_cause_identifier() -> Step:
    """Create the root cause identification stage."""
    agent = create_agent(
        name="Cause Identifier", 
        slug="investigator",
        output_schema=SelectedCause,
        enable_reasoning_tools=False,  # Disabled - Pollinations models misformat
    )
    
    return Step(
        name="2. Identify ONE Cause",
        agent=agent,
        description="Investigate root causes and SELECT the SINGLE most critical factor.",
    )


# =============================================================================
# Stage 3: Department Mapping
# =============================================================================
def create_department_mapper() -> Step:
    """Create the responsible department mapping stage."""
    agent = create_agent(
        name="Department Mapper",
        slug="bureaucrat", 
        output_schema=SelectedDepartment,
        enable_reasoning_tools=False,  # Disabled - Pollinations models misformat
    )
    
    return Step(
        name="3. Map ONE Department",
        agent=agent,
        description="Map government bodies and SELECT the ONE most responsible department.",
    )


# =============================================================================
# Stage 4: Solution Design
# =============================================================================
def create_solution_designer() -> Step:
    """Create the solution design stage."""
    agent = create_agent(
        name="Solution Designer",
        slug="engineer",
        output_schema=SelectedSolution,
        enable_reasoning_tools=False,  # Disabled - Pollinations models misformat
    )
    
    return Step(
        name="4. Design ONE Solution",
        agent=agent,
        description="Evaluate interventions and SELECT the SINGLE most effective solution.",
    )


# =============================================================================
# Stage 5: Funding Match
# =============================================================================
def create_funding_matcher() -> Step:
    """Create the funding matching stage."""
    agent = create_agent(
        name="Funding Matcher",
        slug="liaison",
        output_schema=SelectedFunding,
        enable_reasoning_tools=False,  # Disabled - Pollinations models misformat
    )
    
    return Step(
        name="5. Match ONE Funding",
        agent=agent,
        description="Search funding sources and SELECT the ONE best-matched programme.",
    )


# =============================================================================
# Stage 6: Blueprint Synthesis
# =============================================================================
def synthesize_blueprint(step_input: StepInput) -> StepOutput:
    """
    Final synthesis step: Combine all singleton selections into a
    cohesive RemediationBlueprint for project launch.
    
    This is a custom function that aggregates the pipeline outputs.
    """
    # Get outputs from previous steps
    previous_outputs = step_input.previous_outputs or []
    
    # Extract singleton selections from each stage
    problem: Optional[SelectedProblem] = None
    cause: Optional[SelectedCause] = None
    department: Optional[SelectedDepartment] = None
    solution: Optional[SelectedSolution] = None
    funding: Optional[SelectedFunding] = None
    
    for output in previous_outputs:
        content = output.content
        if isinstance(content, SelectedProblem):
            problem = content
        elif isinstance(content, SelectedCause):
            cause = content
        elif isinstance(content, SelectedDepartment):
            department = content
        elif isinstance(content, SelectedSolution):
            solution = content
        elif isinstance(content, SelectedFunding):
            funding = content
    
    # Synthesize the final blueprint
    if all([problem, cause, department, solution, funding]):
        blueprint = RemediationBlueprint(
            problem=problem,
            cause=cause,
            department=department,
            solution=solution,
            funding=funding,
            project_title=f"{solution.solution_title} for {problem.title}",
            executive_summary=(
                f"This project addresses {problem.title} in {problem.location} "
                f"by tackling the root cause of {cause.cause_title}. "
                f"The {solution.solution_title} approach will be implemented by {department.name} "
                f"with funding from {funding.programme_name}."
            ),
            total_budget_estimate=solution.estimated_cost_tier,
            pilot_phase_scope=f"Initial pilot in {problem.location}",
            key_stakeholders=f"{department.name}, {funding.organization}",
            next_steps=(
                f"1. Engage {department.name} for formal partnership. "
                f"2. Submit application to {funding.programme_name}. "
                f"3. Prepare pilot scope for {problem.location}."
            ),
        )
        return StepOutput(content=blueprint)
    else:
        return StepOutput(content="Error: Missing outputs from previous stages")


# =============================================================================
# Main Pipeline Factory
# =============================================================================
def create_singleton_pipeline() -> Workflow:
    """
    Create the converging singleton pipeline for civic remediation.
    
    Each stage receives the previous output and MUST select exactly ONE item:
    1. Problem → Select ONE critical civic problem
    2. Cause → Identify ONE root cause  
    3. Department → Map ONE responsible body
    4. Solution → Design ONE intervention
    5. Funding → Match ONE funding programme
    6. Blueprint → Synthesize into project launch
    
    Returns:
        Workflow configured for converging singleton outputs
    """
    return Workflow(
        name="Civic Remediation Singleton Pipeline",
        description=(
            "Converging pipeline that narrows down from many options to exactly ONE "
            "at each stage: ONE problem, ONE cause, ONE department, ONE solution, "
            "ONE funding programme, leading to a focused project launch."
        ),
        steps=[
            create_problem_selector(),
            create_cause_identifier(),
            create_department_mapper(),
            create_solution_designer(),
            create_funding_matcher(),
            Step(
                name="6. Synthesize Blueprint",
                executor=synthesize_blueprint,
                description="Combine all singleton selections into final project blueprint.",
            ),
        ],
    )


__all__ = ['create_singleton_pipeline', 'RemediationBlueprint']
