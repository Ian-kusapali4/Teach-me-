import unittest
from unittest.mock import MagicMock, patch
from nodes.learning.evaluator import evaluator_node

class TestEvaluatorNode(unittest.TestCase):

    def setUp(self):
        # Mock subtopic
        mock_topic = MagicMock()
        mock_topic.title = "LangGraph State"
        
        self.state = {
            "syllabus": [mock_topic],
            "current_topic_index": 0,
            "subtopic_content": "State is a TypedDict passed between nodes.",
            "user_input": "State is a dictionary used to store data in the graph.",
            "attempt_count": 0
        }

    @patch('nodes.learning.evaluator.get_model')
    @patch('nodes.learning.evaluator.load_node_prompt')
    def test_evaluator_mastery_success(self, mock_load, mock_model):
        mock_load.return_value = {"system_prompt": "You are a grader."}
        
        # 1. Mock structured output (Challenge & Rubric)
        mock_eval_data = MagicMock()
        mock_eval_data.hidden_rubric = "Check for mention of TypedDict and flow."
        
        mock_llm = mock_model.return_value
        mock_llm.with_structured_output.return_value.invoke.return_value = mock_eval_data
        
        # 2. Mock Grading Response (Score 90)
        mock_grading_res = MagicMock()
        mock_grading_res.content = "Score: 90. Great job explaining the dictionary aspect."
        mock_llm.invoke.return_value = mock_grading_res

        # Run Node
        result = evaluator_node(self.state)

        # Assertions
        self.assertEqual(result["last_score"], 90)
        self.assertEqual(result["attempt_count"], 0) # Mastered, so count stays/resets to 0

    def test_parse_score_helper(self):
        from nodes.learning.evaluator import _parse_score
        self.assertEqual(_parse_score("The user gets a 85/100"), 85)
        self.assertEqual(_parse_score("95 points awarded"), 95)
        self.assertEqual(_parse_score("Fail. 30"), 30)