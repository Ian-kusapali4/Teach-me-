import unittest
from unittest.mock import MagicMock, patch
from nodes.blueprint.goal_setter import goal_setter_node 

class TestGoalSetter(unittest.TestCase):

    def setUp(self):
        self.initial_state = {
            "user_input": "I want to learn dictionaries in Python.",
            "history_summary": "Initial conversation."
        }

    # IMPORTANT: Patch the functions INSIDE the goal_setter module
    @patch('nodes.blueprint.goal_setter.get_model')
    @patch('nodes.blueprint.goal_setter.load_node_prompt')
    @patch('nodes.blueprint.goal_setter.format_prompt')
    def test_recursive_path(self, mock_format, mock_load, mock_model):
        """Tests the logic when the LLM returns PENDING."""
        mock_load.return_value = {"system_prompt": "test"}
        mock_format.return_value = "formatted"
        
        mock_response = MagicMock()
        mock_response.content = "[STATUS]: PENDING\n[MESSAGE]: Tell me more."
        mock_model.return_value.invoke.return_value = mock_response

        result = goal_setter_node(self.initial_state)

        print("\n--- TEST: RECURSIVE PATH ---")
        print(f"Result: {result}")
        self.assertFalse(result["is_approved"])

    @patch('nodes.blueprint.goal_setter.get_model')
    @patch('nodes.blueprint.goal_setter.load_node_prompt')
    @patch('nodes.blueprint.goal_setter.format_prompt')
    def test_synthesis_path(self, mock_format, mock_load, mock_model):
        """Tests the logic when the LLM returns APPROVED."""
        mock_load.return_value = {"system_prompt": "test"}
        mock_format.return_value = "formatted"
        
        mock_response = MagicMock()
        mock_response.content = "[STATUS]: APPROVED\nTerminal Objective: Build an AI Agent."
        mock_model.return_value.invoke.return_value = mock_response

        result = goal_setter_node(self.initial_state)

        print("\n--- TEST: SYNTHESIS PATH ---")
        print(f"Result: {result}")
        self.assertTrue(result["is_approved"])

if __name__ == "__main__":
    unittest.main()