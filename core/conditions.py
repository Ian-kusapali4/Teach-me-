from core.schemas import GraphState

# --- 1. PHASE 1 LOGIC (Blueprint) ---

def should_continue_to_researcher(state: GraphState) -> str:
    """Checks if the Goal_Setter has enough info to move to Research."""
    if state.get("is_approved"):
        return "researcher"
    return "goal_setter"

def check_syllabus_approval(state: GraphState) -> str:
    """Decides if the Architect's syllabus is grounded and ready."""
    if state.get("is_approved"):
        # Reset attempt_count so Phase 2 (The Learning Loop) starts fresh
        state["attempt_count"] = 0
        return "instructor"
    return "architect"

# --- 2. PHASE 2 LOGIC (The Learning Loop) ---

def check_mastery(state: GraphState) -> str:
    """The 'Traffic Controller' for the atomic learning loop."""
    score = state.get("last_score", 0)
    current_index = state.get("current_topic_index", 0)
    total_topics = len(state.get("syllabus", []))

    # CASE A: User Failed (Score < 80)
    if score < 80:
        return "remediate"

    # CASE B: User Passed and there are more topics left
    if score >= 80 and (current_index + 1) < total_topics:
        # ATOMIC UPDATE: Move to the next subtopic in the syllabus
        state["current_topic_index"] = current_index + 1
        return "next_topic"

    # CASE C: User Passed the final subtopic
    return "capstone"

# --- 3. PHASE 3 LOGIC (The Mastery Edge) ---

def evaluate_capstone_result(state: GraphState) -> str:
    """Final decision: Did they pass the whole course?"""
    if state.get("is_complete"):
        return "final_review"
    
    # THE MASTERY EDGE: Reset index so user starts at 0 for the recovery path
    state["current_topic_index"] = 0
    return "architect"

# --- 4. GLOBAL UTILITIES ---

def is_graph_complete(state: GraphState) -> bool:
    """Simple check for the final termination."""
    return state.get("is_complete", False)