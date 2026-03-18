from langgraph.graph import StateGraph, END
from core.schemas import GraphState
from core.conditions import should_continue_to_researcher, check_mastery, is_syllabus_complete
from nodes.blueprint.goal_setter import goal_setter_node
from nodes.blueprint.researcher import researcher_node
from nodes.blueprint.architect import architect_node
from nodes.blueprint.critic_syllabus import critic_syllabus_node
from nodes.learning.instructor import instructor_node
from nodes.learning.evaluator import evaluator_node
from nodes.learning.remediator import remediator_node
from nodes.proof.capstone_gen import capstone_gen_node
from nodes.proof.critic_project import critic_project_node
from nodes.proof.final_review import final_review_node

def create_learning_graph():
    # 1. Initialize the Graph with our Schemas
    workflow = StateGraph(GraphState)

    # 2. Add Phase 1 Nodes: The Blueprint
    workflow.add_node("goal_setter", goal_setter_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("architect", architect_node)
    workflow.add_node("critic_syllabus", critic_syllabus_node)

    # 3. Add Phase 2 Nodes: The Learning Loop
    workflow.add_node("instructor", instructor_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("remediator", remediator_node)

    # 4. Add Phase 3 Nodes: The Proof
    workflow.add_node("capstone_gen", capstone_gen_node)
    workflow.add_node("critic_project", critic_project_node)
    workflow.add_node("final_review", final_review_node)

    # --- 5. DEFINE THE EDGES (The Flow) ---

    workflow.set_entry_point("goal_setter")

    # Phase 1 Transitions
    workflow.add_conditional_edges(
        "goal_setter",
        should_continue_to_researcher,
        {"researcher": "researcher", "goal_setter": "goal_setter"}
    )
    workflow.add_edge("researcher", "architect")
    workflow.add_edge("architect", "critic_syllabus")
    
    # Syllabus Logic: If Critic fails, go back to Architect
    workflow.add_conditional_edges(
        "critic_syllabus",
        lambda state: "architect" if not state.get("is_approved") else "instructor",
        {"architect": "architect", "instructor": "instructor"}
    )

    # Phase 2 Transitions: The Mastery Loop
    workflow.add_edge("instructor", "evaluator")
    workflow.add_conditional_edges(
        "evaluator",
        check_mastery, 
        {
            "next_topic": "instructor",   # Loop to next subtopic
            "remediate": "remediator",    # Fail -> Strategize
            "capstone": "capstone_gen"    # All subtopics done
        }
    )
    workflow.add_edge("remediator", "instructor")

    # Phase 3 Transitions: Graduation or Recovery
    workflow.add_edge("capstone_gen", "critic_project")
    workflow.add_conditional_edges(
        "critic_project",
        lambda state: "final_review" if state.get("is_complete") else "architect",
        {"final_review": "final_review", "architect": "architect"}
    )

    workflow.add_edge("final_review", END)

    return workflow.compile()