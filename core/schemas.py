from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field

# --- 1. SUB-MODELS (Helper Structures) ---

class Subtopic(BaseModel):
    """The individual 'Atomic' units of the syllabus."""
    title: str = Field(description="Action-oriented title of the subtopic.")
    goal: str = Field(description="The specific micro-skill to be mastered.")
    references: List[str] = Field(description="List of URL strings/snippets mapped to this topic.")

class SourceMaterial(BaseModel):
    """The verified data gathered by the Researcher."""
    url: str
    snippet: str
    is_authoritative: bool

# --- 2. NODE-SPECIFIC OUTPUT SCHEMAS (For Structured LLM Responses) ---

class SyllabusOutput(BaseModel):
    """Strict output for Node 3: The Architect."""
    syllabus: List[Subtopic] = Field(description="A logical sequence of 3-5 subtopics.")

class EvaluationOutput(BaseModel):
    """Strict output for Node 6: The Evaluator."""
    challenge: str = Field(description="The quiz or code task for the user.")
    hidden_rubric: str = Field(description="The ideal answer used for grading.")
    
class GradingOutput(BaseModel):
    """Strict output for Node 6 (Grading) and Node 9 (Capstone)."""
    score: int = Field(ge=0, le=100, description="Numerical score of the response.")
    critique: str = Field(description="Detailed feedback on errors or successes.")

class RemediationOutput(BaseModel):
    """Strict output for Node 7: The Remediator."""
    strategy: str = Field(description="A single-sentence pedagogical pivot instruction.")

# --- 3. THE MAIN GRAPH STATE (The "Global" State) ---

class GraphState(TypedDict):
    """
    The Single Source of Truth for the LangGraph workflow.
    This dict defines what every node can read/write.
    """
    # Phase 1: Blueprint
    terminal_objective: str
    source_material: List[SourceMaterial]
    syllabus: List[Subtopic]
    is_approved: bool
    
    # Phase 2: Learning
    current_topic_index: int
    subtopic_content: str
    remediation_strategy: Optional[str]
    
    # Phase 3: Evaluation & Logic
    last_score: int
    last_critique: str
    attempt_count: int
    
    # Finalization
    project_prompt: str
    grading_rubric: str
    is_complete: bool
    history_summary: str  # Keeps the context window lean