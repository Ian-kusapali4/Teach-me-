import os
from dotenv import load_dotenv
from nodes.learning.remediator import remediator_node

load_dotenv()

def test_live_remediation_pivot():
    print("--- STARTING LIVE REMEDIATOR TEST ---")
    
    # Case: User failed twice (Attempt 2)
    # They are clearly stuck on the syntax for LangGraph edges.
    state = {
        "attempt_count": 2,
        "last_critique": "User is trying to use .add_edge() but is missing the required keys.",
        "user_input": "graph.add_edge('node_a')", 
        "hidden_rubric": "Edges require a source, a target, and optionally a mapping."
    }
    
    try:
        result = remediator_node(state)
        
        print(f"\nDIAGNOSIS COMPLETE")
        print(f"FAILED ATTEMPT: {state['attempt_count']}")
        print(f"NEW STRATEGY: {result['remediation_strategy']}")
        
        # Log check to see if it pivoted to a more helpful strategy
        if "Analogy" in result['remediation_strategy'] or "Breakdown" in result['remediation_strategy']:
            print("\n✅ SUCCESS: Model identified the need for a simplified explanation.")
        else:
            print("\nℹ️ NOTE: Model maintained a technical strategy.")
            
    except Exception as e:
        print(f"❌ REMEDIATOR FAILED: {e}")

if __name__ == "__main__":
    test_live_remediation_pivot()