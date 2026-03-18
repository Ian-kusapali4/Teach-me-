from typing import Dict, Any
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState

def final_review_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the Final Review Node.
    Synthesizes the Mastery Report and provides a strategic roadmap for next steps.
    """
    # 1. SETUP: Load Mentor Persona
    prompt_data = load_node_prompt("proof", "final_review")
    # Using 8B/70B depends on the depth of the "Adjacent Topics" search
    llm = get_model("final_review") 
    
    # 2. READ: Context from the completed journey
    terminal_objective = state.get("terminal_objective")
    syllabus = state.get("syllabus", [])
    history_summary = state.get("history_summary", "")
    final_score = state.get("last_score", 0)

    # 3. AUDIT THE JOURNEY & SYNTHESIZE REPORT
    # We pass the full history so the LLM can identify "Atomic Wins"
    formatted_prompt = format_prompt(
        prompt_data["system_prompt"], 
        terminal_objective=terminal_objective,
        syllabus=str([topic.title for topic in syllabus]),
        history_summary=history_summary,
        final_score=final_score
    )
    
    # 4. GENERATE THE MASTERY REPORT
    print(f"--- [FINAL REVIEW] Completing session for: {terminal_objective} ---")
    
    response = llm.invoke([
        ("system", formatted_prompt),
        ("user", "Summarize my progress and give me my next steps.")
    ])
    
    report_content = response.content

    # 5. TERMINATION (Final State)
    # We update the history_summary one last time with the full report
    return {
        "is_complete": True,
        "history_summary": history_summary + f"\n\n--- FINAL MASTERY REPORT ---\n{report_content}",
        # Clear the ephemeral variables to signal a clean exit
        "last_critique": "Session Successfully Completed.",
        "remediation_strategy": None
    }