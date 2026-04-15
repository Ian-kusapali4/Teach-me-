import os
from dotenv import load_dotenv
from nodes.blueprint.goal_setter import goal_setter_node

load_dotenv()
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

def run_live_test(test_name, user_input, history="None yet."):
    print(f"\n{'='*20} TEST: {test_name} {'='*20}")
    print(f"INPUT: {user_input}")
    
    # Create the state object
    state = {
        "user_input": user_input,
        "history_summary": history
    }
    
    # This now calls your actual llm.invoke()
    try:
        result = goal_setter_node(state)
        
        print(f"\nAI RESPONSE (last_critique):\n{result.get('last_critique')}")
        print(f"\nIS APPROVED: {result.get('is_approved')}")
        
        if result.get('is_approved'):
            print(f"TERMINAL OBJECTIVE: {result.get('terminal_objective')}")
            
    except Exception as e:
        print(f"ERROR: {e}")

# --- SCENARIO 1: The Vague Goal (Should result in PENDING) ---
run_live_test(
    "VAGUE GOAL", 
    "I want to learn AI."
)

# --- SCENARIO 2: The Specific Goal (Should result in APPROVED) ---
run_live_test(
    "SPECIFIC GOAL", 
    "I want to learn how to add a single node to a LangGraph StateGraph using the add_node method."
)

# --- SCENARIO 3: The Follow-up (Testing with History) ---
run_live_test(
    "FOLLOW-UP", 
    "I'll use the Groq Llama3-70b model for the backend.",
    history="AI asked what model stack the user is using."
)