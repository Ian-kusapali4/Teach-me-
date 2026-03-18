from typing import Dict, Any, List
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState, SyllabusOutput

def architect_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the Syllabus Architect.
    Reverse-engineers the Terminal Objective into 3-5 atomic steps 
    grounded in the Source Material.
    """
    # 1. SETUP: Load Architect Persona
    prompt_data = load_node_prompt("blueprint", "architect")
    # We use the 'Logic Heavy' model (70B) for structural planning
    llm = get_model("architect") 
    
    # 2. READ: Prep the context for the LLM
    # We pass the research snippets so the Architect knows what is 'teachable'
    formatted_prompt = format_prompt(
        prompt_data["system_prompt"], 
        terminal_objective=state.get("terminal_objective"),
        source_material=str(state.get("source_material", [])),
        user_input=state.get("user_input")
    )
    
    # 3. ANALYZE & CHUNK: The LLM generates the structured syllabus
    # We use .with_structured_output if your LangChain/Groq setup is configured 
    # for the SyllabusOutput Pydantic class.
    response = llm.with_structured_output(SyllabusOutput).invoke(formatted_prompt)
    
    # 4. VALIDATE SOURCE INTEGRITY:
    # Check if any subtopic was flagged as 'missing data' by the LLM logic
    syllabus_list = response.subtopics
    missing_data_flag = False
    missing_query = ""

    for topic in syllabus_list:
        if not topic.refs:
            missing_data_flag = True
            missing_query = f"Need specific documentation for: {topic.title} - {topic.goal}"
            break

    # 5. BRANCHING: If data is missing, we loop back to Researcher
    if missing_data_flag:
        print(f"--- [ARCHITECT] Knowledge Gap Found! Requesting: {missing_query} ---")
        return {
            "last_critique": missing_query,
            "is_approved": False # This triggers the core/conditions logic to loop back
        }

    # 6. INJECT: Update the State
    print(f"--- [ARCHITECT] Syllabus created with {len(syllabus_list)} topics. ---")
    
    return {
        "syllabus": syllabus_list,
        "current_topic_index": 0,
        "is_approved": True,
        "history_summary": f"Architected a {len(syllabus_list)}-step path."
    }