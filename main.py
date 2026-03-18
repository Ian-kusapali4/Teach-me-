import uuid
import sys
from core.graph import create_learning_graph
from core.schemas import GraphState

def run_indigo():
    """
    Entry point for the Project Indigo Autonomous Learning Engine.
    """
    # 1. Compile the Graph
    app = create_learning_graph()
    
    # 2. Initialize Session
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    print("\n" + "="*50)
    print("🤖 PROJECT INDIGO: ADAPTIVE LEARNING SYSTEM")
    print("="*50)
    
    user_input = input("\nWhat technical skill do you want to master today? \n> ")

    # 3. Define the Initial State
    state: GraphState = {
        "user_input": user_input,
        "terminal_objective": "",
        "source_material": [],
        "syllabus": [],
        "is_approved": False,
        "current_topic_index": 0,
        "subtopic_content": "",
        "remediation_strategy": "Direct Technical Instruction",
        "last_score": 0,
        "last_critique": "",
        "attempt_count": 0,
        "project_prompt": "",
        "grading_rubric": "",
        "is_complete": False,
        "history_summary": "",
        "hidden_rubric": ""
    }

    # 4. Execute the Graph Loop
    # We loop until the 'is_complete' flag is set to True
    while not state.get("is_complete"):
        # We stream the events from the current state
        events = app.stream(state, config, stream_mode="values")
        
        for event in events:
            # Update local state with the latest values from the graph
            state.update(event)
            
            # --- NODE-SPECIFIC INTERACTION LOGIC ---
            
            # 1. GOAL SETTING INTERVIEW
            if not state.get("is_approved") and not state.get("terminal_objective"):
                print(f"\nIndigo: {state.get('last_critique', 'Let me clarify...')}")
                state["user_input"] = input("Your Response: ")
                break # Re-run stream with new user input
            
            # 2. THE LESSON DELIVERY
            if state.get("subtopic_content") and state.get("last_score") == 0:
                print(f"\n--- [LESSON] ---\n{state['subtopic_content']}")
                print(f"\n--- [CHALLENGE] ---\n{state.get('last_critique', 'Please complete the task.')}")
                state["user_input"] = input("\nYour Solution: ")
                break 

            # 3. CAPSTONE DELIVERY
            if state.get("project_prompt") and not state.get("is_complete"):
                print(f"\n--- 🏆 FINAL CAPSTONE PROJECT ---\n{state['project_prompt']}")
                state["user_input"] = input("\nUpload Solution (Paste Code/Text): ")
                break

    print("\n--- ✅ SESSION COMPLETE ---")
    print(state.get("history_summary"))

if __name__ == "__main__":
    try:
        run_indigo()
    except KeyboardInterrupt:
        print("\n\nSession terminated by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")