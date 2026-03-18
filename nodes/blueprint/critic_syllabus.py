from typing import Dict, Any
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState

def critic_syllabus_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the Syllabus Critic.
    Audits the Architect's work for Grounding, Fluff, and Density.
    """
    # 1. SETUP: Load Critic Persona
    prompt_data = load_node_prompt("blueprint", "critic_syllabus")
    # Using 70B for high-precision auditing
    llm = get_model("critic_syllabus") 
    
    # 2. INCREMENT: Prevent Infinite Loops
    # We track how many times the Critic has rejected the Architect
    current_retry = state.get("attempt_count", 0) + 1
    
    # 3. READ: Prepare the context for the Audit
    formatted_prompt = format_prompt(
        prompt_data["system_prompt"], 
        terminal_objective=state.get("terminal_objective"),
        syllabus=str(state.get("syllabus", [])),
        source_material=str(state.get("source_material", []))
    )
    
    # 4. PERFORM AUDIT: LLM evaluates based on Audit A, B, and C
    response = llm.invoke(formatted_prompt)
    critique_content = response.content

    # 5. DECISION GATE (The "Bouncer" Logic)
    # We look for the 'is_approved' flag in the structured output or text
    is_valid = "APPROVED" in critique_content.upper() or "is_approved: True" in critique_content.lower()

    if is_valid:
        print(f"--- [CRITIC] Syllabus Approved on Attempt {current_retry}. ---")
        return {
            "is_approved": True,
            "attempt_count": 0, # Reset for the next phase (Learning)
            "last_critique": "Syllabus Verified."
        }
    
    else:
        # Check if we've hit the Fatal Error threshold (3 retries)
        if current_retry >= 3:
            print(f"--- [CRITIC] FATAL ERROR: Architect failed to fix syllabus 3 times. ---")
            return {
                "is_approved": False,
                "is_complete": False,
                "last_critique": "Fatal Architect Error: The current goal cannot be grounded in research. Please re-scope.",
                "attempt_count": 0,
                "current_node": "goal_setter" # Logic to force exit to start
            }
        
        # Standard Rejection: Send back to Architect with the Correction_List
        print(f"--- [CRITIC] Syllabus Rejected (Attempt {current_retry}). Sending back to Architect. ---")
        return {
            "is_approved": False,
            "last_critique": critique_content, # This is the "Correction_List"
            "attempt_count": current_retry
        }