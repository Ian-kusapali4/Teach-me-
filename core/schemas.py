from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field

# --- 1. SUB-MODELS ---

class Subtopic(BaseModel):
    """The individual 'Atomic' units of the syllabus."""
    title: str = Field(description="Action-oriented title of the subtopic.")
    goal: str = Field(description="The specific micro-skill to be mastered.")
    refs: List[str] = Field(default_factory=list, description="URLs or snippets mapped to this topic.")

class SourceMaterial(BaseModel):
    """The verified data gathered by the Researcher."""
    url: str
    snippet: str
    is_authoritative: bool = True

# --- 2. NODE-SPECIFIC OUTPUT SCHEMAS ---

class SyllabusOutput(BaseModel):
    """Output for Node 3: The Architect."""
    subtopics: List[Subtopic] = Field(description="A logical sequence of 3-5 subtopics.")

class EvaluationOutput(BaseModel):
    """Output for Node 6: The Evaluator."""
    challenge: str = Field(description="The quiz or code task for the user.")
    hidden_rubric: str = Field(description="The ideal answer/checklist used for grading.")

class RemediationOutput(BaseModel):
    """Output for Node 7: The Remediator."""
    strategy: str = Field(description="A single-sentence pedagogical pivot instruction.")

class CapstoneOutput(BaseModel):
    """Output for Node 8: The Capstone Generator."""
    prompt: str = Field(description="The final integrated project description.")
    grading_rubric: str = Field(description="The 'Gold Standard' checklist for Node 9.")

class ProjectAuditOutput(BaseModel):
    """Output for Node 9: The Critic (Project)."""
    score: int = Field(ge=0, le=100)
    success_report: str = Field(description="Highlights of what the user did well.")
    failure_critique: str = Field(description="Detailed explanation of gaps if score < 80.")
    failed_subtopic_indices: List[int] = Field(
        default_factory=list, 
        description="Indices of subtopics from the syllabus that need re-teaching."
    )

# --- 3. THE MAIN GRAPH STATE ---

class GraphState(TypedDict):
    """The Single Source of Truth for the Project Indigo workflow."""
    # Phase 1: Blueprint
    user_input: str
    terminal_objective: str
    source_material: List[SourceMaterial]
    syllabus: List[Subtopic]
    is_approved: bool # Used for HITL and Syllabus Validation
    
    # Phase 2: Learning
    current_topic_index: int
    subtopic_content: str
    remediation_strategy: Optional[str]
    hidden_rubric: str # Carry-over from Evaluator to Remediator
    
    # Phase 3: Evaluation & Logic
    last_score: int
    last_critique: str
    attempt_count: int # Tracks retries for both quizzes and syllabus audits
    
    # Finalization
    project_prompt: str
    grading_rubric: str
    is_complete: bool
    history_summary: str