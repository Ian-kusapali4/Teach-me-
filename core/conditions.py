from core.schemas import GraphState

# --- 1. PHASE 1 LOGIC (Blueprint) ---

def should_continue_to_researcher(state: GraphState) -> str:
    """
    Checks if the Goal_Setter has enough info to move to Research.
    If not approved, it loops back to the Goal_Setter for more questions.
    """
    if state.get("is_approved"):
        return "researcher"
    return "goal_setter"

def check_syllabus_approval(state: GraphState) -> str:
    """
    Decides if the Architect's syllabus is grounded and ready.
    If the Critic fails it, we go back to the Architect to fix it.
    """
    if state.get("is_approved"):
        return "instructor"
    return "architect"

# --- 2. PHASE 2 LOGIC (The Learning Loop) ---

def check_mastery(state: GraphState) -> str:
    """
    The 'Traffic Controller' for the atomic learning loop.
    Determines if the user advances, remediates, or finishes.
    """
    score = state.get("last_score", 0)
    current_index = state.get("current_topic_index", 0)
    total_topics = len(state.get("syllabus", []))

    # Case A: User Failed (Score < 80)
    if score < 80:
        return "remediate"

    # Case B: User Passed and there are more topics left
    if score >= 80 and (current_index + 1) < total_topics:
        # Note: The logic to increment the index happens in the Evaluator node 
        # before this condition is called.
        return "next_topic"

    # Case C: User Passed the final subtopic
    return "capstone"

# --- 3. PHASE 3 LOGIC (The Mastery Edge) ---

def evaluate_capstone_result(state: GraphState) -> str:
    """
    Final decision: Did they pass the whole course?
    If they fail, they are sent back to the Architect to rebuild a 'Recovery Syllabus'.
    """
    if state.get("is_complete"):
        return "final_review"
    
    # The 'Mastery Edge' - sends them back to the start of the Architect phase
    return "architect"

# --- 4. GLOBAL UTILITIES ---

def is_graph_complete(state: GraphState) -> bool:
    """Simple check for the final termination."""
    return state.get("is_complete", False)