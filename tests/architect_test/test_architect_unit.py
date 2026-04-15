import unittest
from unittest.mock import MagicMock, patch
from nodes.blueprint.architect import architect_node

class TestArchitectNode(unittest.TestCase):

    def setUp(self):
        # Mocking the state coming from the Researcher
        self.state = {
            "terminal_objective": "Learn LangGraph StateGraphs",
            "source_material": [
                {"url": "https://docs.com", "content": "How to use add_node and add_edge"}
            ],
            "user_input": "I want to learn code syntax."
        }

    @patch('nodes.blueprint.architect.get_model')
    @patch('nodes.blueprint.architect.load_node_prompt')
    def test_architect_success(self, mock_load, mock_model):
        # 1. Setup Mocks
        mock_load.return_value = {"system_prompt": "You are a syllabus architect."}
        
        # Mocking SyllabusOutput Pydantic response
        mock_subtopic = MagicMock()
        mock_subtopic.title = "Step 1: Nodes"
        mock_subtopic.goal = "Understand add_node"
        mock_subtopic.refs = ["https://docs.com"] # Has reference
        
        mock_response = MagicMock()
        mock_response.subtopics = [mock_subtopic]
        
        # Configure the structured output chain
        mock_llm = mock_model.return_value
        mock_llm.with_structured_output.return_value.invoke.return_value = mock_response

        # 2. Run Node
        result = architect_node(self.state)

        # 3. Assertions
        self.assertTrue(result["is_approved"])
        self.assertEqual(len(result["syllabus"]), 1)
        self.assertEqual(result["current_topic_index"], 0)

    @patch('nodes.blueprint.architect.get_model')
    def test_architect_knowledge_gap(self, mock_model):
        # Setup response with NO refs (Simulating missing data)
        mock_subtopic = MagicMock()
        mock_subtopic.refs = [] # Empty list triggers missing_data_flag
        
        mock_response = MagicMock()
        mock_response.subtopics = [mock_subtopic]
        
        mock_llm = mock_model.return_value
        mock_llm.with_structured_output.return_value.invoke.return_value = mock_response

        # Run Node
        result = architect_node(self.state)

        # 3. Assertions
        self.assertFalse(result["is_approved"])
        self.assertIn("Need specific documentation", result["last_critique"])