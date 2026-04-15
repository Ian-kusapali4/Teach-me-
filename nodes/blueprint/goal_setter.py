from typing import Dict, Any
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState

def goal_setter_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the Goal_Setter Logic Flow.
    Handles the Drill-Down (Recursive) vs. Synthesis (Exit) transitions.
    """
    # 1. Setup: Load Prompt and Model
    prompt_data = load_node_prompt("blueprint", "goal_setter")
    llm = get_model("goal_setter")
    
    # 2. READ & ANALYZE (Injecting current state into the template)
    formatted_system = format_prompt(
        prompt_data["system_prompt"], 
        user_input=state.get("user_input"),
        history_summary=state.get("history_summary", "None yet.")
    )
    
    # 3. EXECUTE LLM CALL
    response = llm.invoke([
        ("system", formatted_system),
        ("user", state.get("user_input"))
    ])
    
    content = response.content
    content_upper = content.upper()
    
    # 4. THE DRILL-DOWN vs. SYNTHESIS LOGIC (Strict Parsing)
    # Check for approval markers anywhere in the text
    is_atomic = any(marker in content_upper for marker in [
        "STATUS: APPROVED", 
        "IS_APPROVED: TRUE", 
        "GOAL IS ATOMIC", 
        "[APPROVED]"
    ])

    # Defensive check: If the LLM explicitly outputs a "False" status, 
    # it overrides any accidental keyword matches.
    if "IS_APPROVED: FALSE" in content_upper or "STATUS: PENDING" in content_upper:
        is_atomic = False

    if not is_atomic:
        # STEP 4: THE DRILL-DOWN (Recursive)
        # Update history with the user's last input and the AI's follow-up
        new_history = state.get("history_summary", "") + f"\nUser: {state.get('user_input')}\nAI: {content}\n"
        
        return {
            "is_approved": False,
            "last_critique": content, 
            "history_summary": new_history
        }
    
    else:
        # STEP 5: THE SYNTHESIS
        # Extract the Terminal Objective string
        if "Terminal Objective:" in content:
            terminal_obj = content.split("Terminal Objective:")[-1].strip()
        else:
            # Fallback if the marker is missing but the status is approved
            terminal_obj = state.get("user_input")
        
        return {
            "terminal_objective": terminal_obj,
            "is_approved": True,
            "last_critique": f"Target Locked: {terminal_obj}",
            "history_summary": "Goal Finalized. Transcript Cleared." 
        }
    # we might also want to consider adding a catch-all else case that handles unexpected outputs, but for now this should cover the main logic flow.
    # we might also need to strip the state management to only return the termianl objective 