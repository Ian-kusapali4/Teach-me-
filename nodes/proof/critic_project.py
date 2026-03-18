from typing import Dict, Any, List
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState, ProjectAuditOutput

def critic_project_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the Project Critic.
    High-stakes code review that triggers the Mastery Edge recovery loop.
    """
    # 1. SETUP: Load Critic Persona
    prompt_data = load_node_prompt("proof", "critic_project")
    # Using 70B for high-precision code review and synthesis audit
    llm = get_model("critic_project") 
    
    # 2. READ: Context for the Audit
    user_submission = state.get("user_input") # The final project code/answer
    rubric = state.get("grading_rubric")
    syllabus = state.get("syllabus", [])

    # 3. MULTIDIMENSIONAL REVIEW (The Audit)
    formatted_prompt = format_prompt(
        prompt_data["system_prompt"], 
        user_submission=user_submission,
        grading_rubric=rubric,
        syllabus=str([topic.title for topic in syllabus])
    )
    
    # 4. EXECUTE AUDIT: The LLM scores the project and maps failures
    audit_data = llm.with_structured_output(ProjectAuditOutput).invoke(formatted_prompt)
    
    score = audit_data.score
    is_passing = score >= 80

    # 5. DECISION GATE & FAILURE ATTRIBUTION
    if is_passing:
        print(f"--- [CRITIC] Project PASSED with score: {score}/100 ---")
        return {
            "is_complete": True,
            "last_score": score,
            "last_critique": audit_data.success_report,
            "history_summary": state.get("history_summary", "") + f"\nPassed Capstone: {score}%"
        }
    
    else:
        # 6. THE MASTERY EDGE (Self-Healing Loop)
        # We identify which subtopics the user failed (e.g., [1, 3])
        failed_indices = audit_data.failed_subtopic_indices
        
        # We PRUNE the syllabus to only include the failed parts for the Architect to fix
        recovery_syllabus = [syllabus[i] for i in failed_indices if i < len(syllabus)]
        
        print(f"--- [CRITIC] Project FAILED ({score}/100). Triggering Mastery Edge. ---")
        print(f"--- [CRITIC] Identifying Gaps in Topics: {failed_indices} ---")

        return {
            "is_complete": False,
            "is_approved": False, # Forces the Architect to re-run
            "syllabus": recovery_syllabus, # The 'Pruned' syllabus for recovery
            "last_score": score,
            "last_critique": audit_data.failure_critique,
            "current_topic_index": 0, # Reset for the recovery loop
            "history_summary": state.get("history_summary", "") + f"\nFailed Capstone: {score}%"
        }