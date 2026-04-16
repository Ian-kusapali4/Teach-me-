import os
from dotenv import load_dotenv
from unittest.mock import MagicMock
from nodes.proof.critic_project import critic_project_node

load_dotenv()

def test_live_project_audit():
    print("--- STARTING LIVE PROJECT CRITIC TEST ---")
    
    # Simulating a real scenario
    state = {
        "user_input": """
from langgraph.graph import StateGraph
workflow = StateGraph(dict)
# Missing edges and nodes!
""",
        "grading_rubric": "1. Define StateGraph. 2. Add at least one node. 3. Add an edge.",
        "syllabus": [
            MagicMock(title="Defining State"),
            MagicMock(title="Adding Nodes"),
            MagicMock(title="Routing Edges")
        ],
        "history_summary": "User finished the curriculum."
    }
    
    try:
        result = critic_project_node(state)
        
        if result["is_complete"]:
            print(f"\n🏆 PASS: {result['last_score']}/100")
            print(f"Report: {result['last_critique']}")
        else:
            print(f"\n🩹 MASTERY EDGE TRIGGERED: {result['last_score']}/100")
            print(f"Audit: {result['last_critique']}")
            print(f"Recovery Syllabus length: {len(result['syllabus'])}")
            for topic in result['syllabus']:
                print(f" - Reteaching: {topic.title}")
            
    except Exception as e:
        print(f"❌ CRITIC FAILED: {e}")

if __name__ == "__main__":
    test_live_project_audit()