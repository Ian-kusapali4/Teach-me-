from typing import Dict, Any
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState, CapstoneOutput

def capstone_gen_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the Capstone Generator Node.
    Synthesizes the entire syllabus into a single, integrated final project.
    """
    # 1. SETUP: Load Capstone Persona
    prompt_data = load_node_prompt("proof", "capstone_gen")
    # Using 70B for high-level architectural synthesis
    llm = get_model("capstone_gen") 
    
    # 2. READ: Context from the entire session
    terminal_objective = state.get("terminal_objective")
    syllabus = state.get("syllabus", [])
    # Collect all lesson content delivered during Phase 2
    history_summary = state.get("history_summary", "") 

    # 3. SYNTHESIZE & PROJECT DRAFTING
    # We pass the full syllabus so the LLM knows exactly which 3-5 subtopics to link
    formatted_prompt = format_prompt(
        prompt_data["system_prompt"], 
        terminal_objective=terminal_objective,
        syllabus=str([topic.title for topic in syllabus]),
        history_summary=history_summary
    )
    
    # 4. GENERATION (The Scenario and the Hidden Rubric)
    # We use a structured output to separate what the user sees from the grading key
    capstone_data = llm.with_structured_output(CapstoneOutput).invoke(formatted_prompt)

    # 5. USER PRESENTATION
    print(f"--- [CAPSTONE] Generating Final Project for: {terminal_objective} ---")
    
    # 6. INJECT (State Update)
    return {
        "project_prompt": capstone_data.prompt,
        "grading_rubric": capstone_data.grading_rubric, # Hidden from the user
        "history_summary": history_summary + "\nCapstone Project Generated."
    }