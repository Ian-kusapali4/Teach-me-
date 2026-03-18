import os
from langchain_groq import ChatGroq
from config import get_config

def get_model(node_name: str):
    """
    Model Factory: Returns a specific Groq model configuration 
    based on the complexity of the node's task.
    """
    config = get_config()
    api_key = config.GROQ_API_KEY
    
    # 1. High-Reasoning Nodes (Need the 'Big' Models)
    # Architect, Critic, Capstone_Gen, Remediator
    logic_heavy_nodes = [
        "architect", 
        "critic_syllabus", 
        "critic_project", 
        "remediator", 
        "capstone_gen"
    ]
    
    # 2. High-Speed / Creative Nodes (Need the 'Fast' Models)
    # Goal_Setter, Researcher, Instructor, Evaluator, Final_Review
    
    if node_name in logic_heavy_nodes:
        # Using Llama 3.3 70B for complex logic/auditing
        return ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.3-70b-specdec",
            temperature=0.1,  # Low temperature for precision
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
    else:
        # Using Llama 3.1 8B or similar for fast synthesis/chat
        return ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.7,  # Higher temperature for teaching/engagement
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

# Example of how a node will call this:
# llm = get_model("instructor")