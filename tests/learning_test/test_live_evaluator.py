import os
from dotenv import load_dotenv
from nodes.learning.evaluator import evaluator_node
from core.schemas import Subtopic

load_dotenv()

def test_live_evaluator():
    print("--- STARTING LIVE EVALUATOR TEST ---")
    
    test_topic = Subtopic(
        title="Python Lists",
        goal="Explain how to append to a list",
        refs=[]
    )
    
    state = {
        "syllabus": [test_topic],
        "current_topic_index": 0,
        "subtopic_content": "To add an item to a list in Python, use the .append() method.",
        "user_input": "I would use the .append() method.", # INCORRECT ANSWER
        "terminal_objective": "Master basic Python list operations",
        "attempt_count": 0
    }
    
    try:
        result = evaluator_node(state)
        
        print(f"\nRUBRIC CREATED: {result['hidden_rubric']}")
        print(f"SCORE GIVEN: {result['last_score']}/100")
        print(f"CRITIQUE: {result['last_critique']}")
        
        if result['last_score'] < 80:
            print("\n❌ STATUS: Failed. Sent to Remediator.")
        else:
            print("\n✅ STATUS: Mastered! Moving to next topic.")
            
    except Exception as e:
        print(f"❌ EVALUATOR FAILED: {e}")

if __name__ == "__main__":
    test_live_evaluator()