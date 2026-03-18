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
    # We pass the full history so the LLM remembers previous interview questions
    formatted_system = format_prompt(
        prompt_data["system_prompt"], 
        user_input=state.get("user_input"),
        history_summary=state.get("history_summary", "None yet.")
    )
    
    # 3. EXECUTE LLM CALL
    # Note: We use structured output if your Groq setup supports it, 
    # otherwise we parse the text for 'is_approved'
    response = llm.invoke([
        ("system", formatted_system),
        ("user", state.get("user_input"))
    ])
    
    content = response.content
    
    # 4. THE DRILL-DOWN vs. SYNTHESIS LOGIC
    # We look for a specific marker or 'is_approved' boolean in the LLM response
    # For this implementation, we assume the LLM outputs a specific format:
    # [STATUS]: APPROVED/PENDING
    # [MESSAGE]: ...
    
    is_atomic = "APPROVED" in content or "is_approved: True" in content.lower()

    if not is_atomic:
        # STEP 4: THE DRILL-DOWN (Recursive)
        # We update the history and the 'last_critique' which acts as the interview question
        new_history = state.get("history_summary", "") + f"\nAI: {content}\n"
        
        return {
            "is_approved": False,
            "last_critique": content, # This will be displayed to the user in main.py
            "history_summary": new_history
        }
    
    else:
        # STEP 5: THE SYNTHESIS
        # Extract the Terminal Objective (usually the text after a marker)
        # Example logic: Terminal_Objective: "By the end of this session..."
        terminal_obj = content.split("Terminal Objective:")[-1].strip()
        
        return {
            "terminal_objective": terminal_obj,
            "is_approved": True,
            "last_critique": f"Target Locked: {terminal_obj}",
            "history_summary": "Goal Finalized. Transcript Cleared." # Step 6: Clear to save tokens
        }