from typing import Dict, Any
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState, RemediationOutput

def remediator_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the Remediator Node.
    Diagnoses why the user failed and selects a new teaching strategy.
    """
    # 1. SETUP: Load Remediator Persona
    prompt_data = load_node_prompt("learning", "remediator")
    # Using 70B for deep pedagogical reasoning and diagnosis
    llm = get_model("remediator") 
    
    # 2. READ: Historical data and failure count
    attempt_count = state.get("attempt_count", 1)
    last_critique = state.get("last_critique", "No critique provided.")
    user_input = state.get("user_input", "") # The failed answer
    hidden_rubric = state.get("hidden_rubric", "")

    # 3. DIAGNOSE & SELECT STRATEGY (The Pivot)
    # We pass the attempt count so the LLM knows which CASE logic to apply
    formatted_prompt = format_prompt(
        prompt_data["system_prompt"], 
        attempt_count=attempt_count,
        last_critique=last_critique,
        user_answer=user_input,
        hidden_rubric=hidden_rubric
    )
    
    # The LLM outputs the strategy string based on your Case 1, 2, or 3 logic
    remediation_data = llm.with_structured_output(RemediationOutput).invoke(formatted_prompt)

    # 4. INJECT (State Update)
    print(f"--- [REMEDIATOR] Attempt {attempt_count} Failed. Strategy Pivot: {remediation_data.strategy} ---")

    return {
        "remediation_strategy": remediation_data.strategy,
        # We don't increment attempt_count here because the Evaluator already did it,
        # but we keep it in the state for the next loop.
    }