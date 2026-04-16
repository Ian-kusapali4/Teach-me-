import unittest
from unittest.mock import MagicMock, patch
from nodes.proof.final_review import final_review_node

class TestFinalReviewNode(unittest.TestCase):

    def setUp(self):
        self.state = {
            "terminal_objective": "Mastering LangGraph",
            "syllabus": [MagicMock(title="Nodes"), MagicMock(title="Edges")],
            "history_summary": "User completed learning and capstone.",
            "last_score": 95
        }

    @patch('nodes.proof.final_review.get_model')
    @patch('nodes.proof.final_review.load_node_prompt')
    def test_final_review_compilation(self, mock_load, mock_model):
        mock_load.return_value = {"system_prompt": "You are a senior career mentor."}
        
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.content = "Great job! Next, you should learn about LangSmith tracing."
        mock_model.return_value.invoke.return_value = mock_response

        # Run Node
        result = final_review_node(self.state)

        # Assertions
        self.assertTrue(result["is_complete"])
        self.assertIn("FINAL MASTERY REPORT", result["history_summary"])
        self.assertIn("LangSmith tracing", result["history_summary"])
        self.assertIsNone(result["remediation_strategy"])