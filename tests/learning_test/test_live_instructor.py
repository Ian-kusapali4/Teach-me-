import os
from dotenv import load_dotenv
from nodes.learning.instructor import instructor_node
from core.schemas import Subtopic # Importing your actual schema

load_dotenv()

def test_live_instructor():
    print("--- STARTING LIVE INSTRUCTOR TEST ---")
    
    # Manually creating a subtopic that mimics your Architect's output
    test_topic = Subtopic(
        title="LangGraph Nodes",
        goal="Explain how to define a node function in Python",
        refs=["https://langchain-ai.github.io/langgraph/"]
    )
    
    state = {
        "syllabus": [test_topic],
        "current_topic_index": 0,
        "remediation_strategy": "Direct Technical Instruction"
    }
    
    try:
        result = instructor_node(state)
        
        print("\n--- GENERATED LESSON CONTENT ---")
        print(result["subtopic_content"])
        print("\n--- STRATEGY STATUS ---")
        print(f"Strategy Reset to: {result['remediation_strategy']}")
            
    except Exception as e:
        print(f"❌ INSTRUCTOR FAILED: {e}")

if __name__ == "__main__":
    test_live_instructor()