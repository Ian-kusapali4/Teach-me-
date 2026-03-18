import os
from langchain_groq import ChatGroq
from config import get_config

def get_model(node_name: str, streaming: bool = False):
    """
    Model Factory: Returns a specific Groq model configuration 
    based on the complexity of the node's task.
    """
    config = get_config()
    api_key = config.GROQ_API_KEY
    
    # 1. High-Reasoning Nodes: Require deep logical synthesis and audit precision.
    # Architecture, Auditing, and Recovery diagnosis.
    logic_heavy_nodes = [
        "architect", 
        "critic_syllabus", 
        "critic_project", 
        "remediator", 
        "capstone_gen"
    ]
    
    # 2. Logic-Heavy Configuration (Llama 3.3 70B)
    if node_name in logic_heavy_nodes:
        return ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.3-70b-specdec",
            temperature=0.1,  # Low for deterministic, logical consistency
            max_tokens=4096,   # Adequate for complex syllabus/critique generation
            timeout=30,
            max_retries=3,
            streaming=streaming
        )
    
    # 3. High-Speed / Creative Configuration (Llama 3.1 8B)
    # Used for Teaching, Quizzing, and Initial Goal Alignment.
    else:
        return ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.6,  # Slightly higher for varied teaching analogies
            max_tokens=2048,   # Atomic lessons stay within this range
            timeout=20,
            max_retries=2,
            streaming=streaming
        )

# Usage Example:
# instructor_llm = get_model("instructor", streaming=True)