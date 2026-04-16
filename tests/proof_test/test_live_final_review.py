import os
from dotenv import load_dotenv
from unittest.mock import MagicMock
from nodes.proof.final_review import final_review_node

load_dotenv()

def test_live_mentor_roadmap():
    print("--- STARTING LIVE FINAL REVIEW TEST ---")
    
    # Simulating a successful journey
    state = {
        "terminal_objective": "Building Autonomous AI Agents with LangGraph",
        "syllabus": [
            MagicMock(title="State Management"),
            MagicMock(title="Conditional Routing"),
            MagicMock(title="Tool Integration")
        ],
        "history_summary": "Phase 1: Research complete. Phase 2: User mastered nodes. Phase 3: Capstone passed with 92%.",
        "last_score": 92
    }
    
    try:
        result = final_review_node(state)
        
        print("\n--- FINAL OUTPUT (HISTORY_SUMMARY) ---")
        # We print just the new part added
        report = result['history_summary'].split("--- FINAL MASTERY REPORT ---")[-1]
        print(report)
        
        if result["is_complete"] and result["remediation_strategy"] is None:
            print("\n✅ SUCCESS: Session terminated cleanly.")
            
    except Exception as e:
        print(f"❌ FINAL REVIEW FAILED: {e}")

if __name__ == "__main__":
    test_live_mentor_roadmap()