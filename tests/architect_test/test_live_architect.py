import os
from dotenv import load_dotenv
from nodes.blueprint.architect import architect_node

load_dotenv()

def test_live_architect():
    print("--- STARTING LIVE ARCHITECT TEST ---")
    
    # Simulating data that we know came from your previous Researcher test
    state = {
        "terminal_objective": "How to implement a StateGraph in LangGraph using Python.",
        "source_material": [
            {"url": "https://docs.com", "content": "StateGraph(State) lets you define nodes and edges."}
        ]
    }
    
    try:
        result = architect_node(state)
        
        if result["is_approved"]:
            print("\n✅ SUCCESS: Syllabus Created")
            for i, topic in enumerate(result["syllabus"], 1):
                print(f"{i}. {topic.title} - Goal: {topic.goal}")
                print(f"   Refs: {topic.refs}")
        else:
            print("\n🔄 LOOP BACK: Architect requested more research.")
            print(f"Reason: {result['last_critique']}")
            
    except Exception as e:
        print(f"❌ ARCHITECT FAILED: {e}")

if __name__ == "__main__":
    test_live_architect()