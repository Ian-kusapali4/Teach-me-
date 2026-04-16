import unittest
from unittest.mock import MagicMock, patch
from nodes.proof.capstone_gen import capstone_gen_node

class TestCapstoneGenNode(unittest.TestCase):

    def setUp(self):
        # Mocking a finished syllabus
        mock_topic_1 = MagicMock(title="Node Definition")
        mock_topic_2 = MagicMock(title="Edge Logic")
        
        self.state = {
            "terminal_objective": "Build a LangGraph Agent",
            "syllabus": [mock_topic_1, mock_topic_2],
            "history_summary": "User mastered nodes and edges."
        }

    @patch('nodes.proof.capstone_gen.get_model')
    @patch('nodes.proof.capstone_gen.load_node_prompt')
    def test_capstone_generation_logic(self, mock_load, mock_model):
        mock_load.return_value = {"system_prompt": "You are a senior architect."}
        
        # Mock the Pydantic output
        mock_output = MagicMock()
        mock_output.prompt = "Create a graph that handles a simple math query."
        mock_output.grading_rubric = "1. Must use StateGraph. 2. Must use edges."
        
        mock_llm = mock_model.return_value
        mock_llm.with_structured_output.return_value.invoke.return_value = mock_output

        # Run Node
        result = capstone_gen_node(self.state)

        # Assertions
        self.assertIn("Create a graph", result["project_prompt"])
        self.assertEqual(result["grading_rubric"], mock_output.grading_rubric)
        self.assertTrue("Capstone Project Generated" in result["history_summary"])