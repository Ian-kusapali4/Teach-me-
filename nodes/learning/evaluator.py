from typing import Dict, Any
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState, EvaluationOutput

def evaluator_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the Evaluator Node.
    Generates a challenge, waits for user input, and grades against a hidden rubric.
    """
    # 1. SETUP: Load Evaluator Persona
    prompt_data = load_node_prompt("learning", "evaluator")
    llm = get_model("evaluator")
    
    # 2. READ: Context from the Syllabus and the Lesson just delivered
    syllabus = state.get("syllabus", [])
    current_index = state.get("current_topic_index", 0)
    current_topic = syllabus[current_index]
    lesson_content = state.get("subtopic_content", "")
    
    # 3. CHALLENGE GENERATION (The "Test")
    # We use structured output to separate the 'challenge' from the 'hidden_rubric'
    formatted_prompt = format_prompt(
        prompt_data["system_prompt"], 
        current_topic_title=current_topic.title,
        subtopic_content=lesson_content,
        terminal_objective=state.get("terminal_objective")
    )
    
    # The LLM generates the task the user sees AND the rubric the user DOES NOT see
    eval_data = llm.with_structured_output(EvaluationOutput).invoke(formatted_prompt)

    # 4. COLLECT USER RESPONSE (Handled by the main.py / Interface)
    # In a LangGraph workflow, the 'evaluator' node usually generates the question, 
    # then the graph 'waits' for the next entry point to provide the user_response.
    
    user_answer = state.get("user_input", "") # This comes from the CLI/Web input
    
    # 5. COMPARATIVE GRADING (The "Check")
    # We call the LLM one more time to act as the "Grader"
    grading_prompt = f"""
    [HIDDEN RUBRIC]: {eval_data.hidden_rubric}
    [USER RESPONSE]: {user_answer}
    
    Grade the response from 0-100 based on Accuracy, Completeness, and Logic.
    Provide a technical critique if they missed anything.
    """
    
    grading_res = llm.invoke(grading_prompt)
    # Logic to parse the score and critique from the text
    # (In production, you'd use a Pydantic parser here as well)
    score = _parse_score(grading_res.content) 
    critique = grading_res.content

    # 6. STATE UPDATE & CONDITIONAL ROUTING
    is_mastered = score >= 80
    new_attempt_count = state.get("attempt_count", 0) + (0 if is_mastered else 1)
    
    print(f"--- [EVALUATOR] Score: {score}/100. Mastery: {is_mastered} ---")

    return {
        "last_score": score,
        "last_critique": critique,
        "attempt_count": new_attempt_count if not is_mastered else 0,
        "hidden_rubric": eval_data.hidden_rubric, # Saved for the Remediator to see
        # We don't increment the index here; the Graph Edges handle the 'Next Topic' move
    }

def _parse_score(text: str) -> int:
    """Helper to extract a numerical score from the LLM's grading text."""
    try:
        # Simple extraction logic: find the first number in the text
        import re
        match = re.search(r'\b([0-9]{1,3})\b', text)
        return int(match.group(1)) if match else 0
    except:
        return 0