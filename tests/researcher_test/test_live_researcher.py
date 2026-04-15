import os
from dotenv import load_dotenv
from nodes.blueprint.researcher import researcher_node

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "false"

def test_live_research():
    print("--- STARTING LIVE RESEARCH TEST ---")
    
    state = {
        "terminal_objective": "How to implement a StateGraph in LangGraph using Python."
    }
    
    try:
        result = researcher_node(state)
        
        print(f"\nQUERY RESULTS SUMMARY:")
        print(result["history_summary"])
        
        print(f"\nTOP SOURCES FOUND:")
        for i, source in enumerate(result["source_material"], 1):
            print(f"{i}. URL: {source['url']}")
            print(f"   Snippet: {source['content'][:100]}...")
            
    except Exception as e:
        print(f"RESEARCH FAILED: {e}")

if __name__ == "__main__":
    test_live_research()