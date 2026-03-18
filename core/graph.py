from langgraph.graph import StateGraph, END
from core.schemas import GraphState
# Import our refined logic gates
from core.conditions import (
    should_continue_to_researcher, 
    check_mastery, 
    check_syllabus_approval
)
# ... (your existing imports)

def create_learning_graph():
    workflow = StateGraph(GraphState)

    # Add Nodes (No changes here)
    workflow.add_node("goal_setter", goal_setter_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("architect", architect_node)
    workflow.add_node("critic_syllabus", critic_syllabus_node)
    workflow.add_node("instructor", instructor_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("remediator", remediator_node)
    workflow.add_node("capstone_gen", capstone_gen_node)
    workflow.add_node("critic_project", critic_project_node)
    workflow.add_node("final_review", final_review_node)

    workflow.set_entry_point("goal_setter")

    # --- REFINED EDGES ---

    # 1. Goal Setting with Pause: Logic check handles the "Interview"
    workflow.add_conditional_edges(
        "goal_setter",
        should_continue_to_researcher,
        {
            "researcher": "researcher", 
            "goal_setter": "goal_setter" # This triggers the loop back
        }
    )

    # 2. Architect's "Research Loop": If Architect needs more data
    workflow.add_conditional_edges(
        "architect",
        lambda state: "researcher" if not state.get("is_approved") else "critic_syllabus",
        {"researcher": "researcher", "critic_syllabus": "critic_syllabus"}
    )

    workflow.add_edge("researcher", "architect")

    # 3. Syllabus Validation (Using the named condition)
    workflow.add_conditional_edges(
        "critic_syllabus",
        check_syllabus_approval, 
        {"architect": "architect", "instructor": "instructor"}
    )

    # 4. Phase 2: The Mastery Loop (No changes, this was perfect)
    workflow.add_edge("instructor", "evaluator")
    workflow.add_conditional_edges(
        "evaluator",
        check_mastery, 
        {
            "next_topic": "instructor",
            "remediate": "remediator",
            "capstone": "capstone_gen"
        }
    )
    workflow.add_edge("remediator", "instructor")

    # 5. Phase 3: Graduation or Recovery
    workflow.add_edge("capstone_gen", "critic_project")
    workflow.add_conditional_edges(
        "critic_project",
        lambda state: "final_review" if state.get("is_complete") else "architect",
        {"final_review": "final_review", "architect": "architect"}
    )

    workflow.add_edge("final_review", END)

    return workflow.compile()