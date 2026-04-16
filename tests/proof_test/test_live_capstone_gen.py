import os
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch
from nodes.proof.capstone_gen import capstone_gen_node

load_dotenv()

def test_live_capstone_synthesis():
    print("--- STARTING LIVE CAPSTONE GENERATOR TEST ---")
    
    # Simulating a state where the user just finished learning LangGraph
    state = {
        "terminal_objective": "Implementing a stateful multi-agent system in LangGraph",
        "syllabus": [
            MagicMock(title="Defining TypedDict State"),
            MagicMock(title="Adding Nodes and Edges"),
            MagicMock(title="Conditional Routing Logic")
        ],
        "history_summary": "Phase 2 Complete. User successfully learned state, nodes, and routing."
    }
    
    try:
        result = capstone_gen_node(state)
        
        print("\n--- THE CAPSTONE CHALLENGE ---")
        print(result["project_prompt"])
        
        print("\n--- INTERNAL GRADING RUBRIC (HIDDEN) ---")
        print(result["grading_rubric"])
            
    except Exception as e:
        print(f"❌ CAPSTONE GEN FAILED: {e}")

if __name__ == "__main__":
    test_live_capstone_synthesis()