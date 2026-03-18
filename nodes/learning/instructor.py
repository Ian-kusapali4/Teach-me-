from typing import Dict, Any
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState

def instructor_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the JIT Instructor.
    Generates a lesson based on the current subtopic and source material.
    """
    # 1. SETUP: Load Instructor Persona
    prompt_data = load_node_prompt("learning", "instructor")
    llm = get_model("instructor") # Using a fast, high-quality model (e.g., Llama 3 8B)
    
    # 2. GATHER CONTEXT: Identify current topic in the syllabus
    syllabus = state.get("syllabus", [])
    current_index = state.get("current_topic_index", 0)
    current_topic = syllabus[current_index]
    
    # DETERMINE MODALITY (The Pivot Check)
    # If the Remediator set a strategy, we override the default
    strategy = state.get("remediation_strategy", "Direct Technical Instruction")
    
    # 3. FILTER Source_Material (Semantic Extraction)
    # We only show the instructor the snippets the Architect mapped to this topic
    relevant_refs = current_topic.refs if hasattr(current_topic, 'refs') else []
    
    # 4. READ: Prepare the instruction prompt
    formatted_prompt = format_prompt(
        prompt_data["system_prompt"], 
        current_topic_title=current_topic.title,
        current_topic_goal=current_topic.goal,
        current_topic_references=str(relevant_refs),
        remediation_strategy=strategy
    )
    
    # 5. SYNTHESIZE CONTENT: Generate the lesson
    print(f"--- [INSTRUCTOR] Teaching: {current_topic.title} using strategy: {strategy} ---")
    
    response = llm.invoke([
        ("system", formatted_prompt),
        ("user", f"Teach me the subtopic: {current_topic.title}")
    ])
    
    lesson_content = response.content

    # 6. INJECT (State Update)
    return {
        "subtopic_content": lesson_content,
        # Step 7: Consume the strategy so it doesn't accidentally 
        # apply to the next topic unless the Remediator sets it again
        "remediation_strategy": "Direct Technical Instruction" 
    }