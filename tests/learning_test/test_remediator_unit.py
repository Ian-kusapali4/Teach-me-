import unittest
from unittest.mock import MagicMock, patch
from nodes.learning.remediator import remediator_node

class TestRemediatorNode(unittest.TestCase):

    def setUp(self):
        self.state = {
            "attempt_count": 1,
            "last_critique": "User confused .append() with .add().",
            "user_input": "my_list.add('item')",
            "hidden_rubric": "Must use the .append() method for Python lists."
        }

    @patch('nodes.learning.remediator.get_model')
    @patch('nodes.learning.remediator.load_node_prompt')
    def test_remediation_strategy_selection(self, mock_load, mock_model):
        mock_load.return_value = {"system_prompt": "You are a pedagogical expert."}
        
        # Mock structured output
        mock_output = MagicMock()
        mock_output.strategy = "Socratic Questioning: Focus on the difference between Sets and Lists."
        
        mock_llm = mock_model.return_value
        mock_llm.with_structured_output.return_value.invoke.return_value = mock_output

        # Run Node
        result = remediator_node(self.state)

        # Assertions
        self.assertEqual(result["remediation_strategy"], "Socratic Questioning: Focus on the difference between Sets and Lists.")