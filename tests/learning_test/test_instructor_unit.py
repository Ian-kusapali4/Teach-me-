import unittest
from unittest.mock import MagicMock, patch
from nodes.learning.instructor import instructor_node

class TestInstructorNode(unittest.TestCase):

    def setUp(self):
        # Mocking a syllabus structure with 2 topics
        mock_topic_0 = MagicMock()
        mock_topic_0.title = "Intro to State"
        mock_topic_0.goal = "Learn variables"
        mock_topic_0.refs = ["https://docs.com/state"]

        self.state = {
            "syllabus": [mock_topic_0],
            "current_topic_index": 0,
            "remediation_strategy": "Analogy-heavy explanation"
        }

    @patch('nodes.learning.instructor.get_model')
    @patch('nodes.learning.instructor.load_node_prompt')
    def test_instructor_teaching_logic(self, mock_load, mock_model):
        mock_load.return_value = {"system_prompt": "You are an instructor."}
        
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.content = "This is your lesson on State."
        mock_model.return_value.invoke.return_value = mock_response

        # Run Node
        result = instructor_node(self.state)

        # Assertions
        self.assertEqual(result["subtopic_content"], "This is your lesson on State.")
        # Verify strategy reset
        self.assertEqual(result["remediation_strategy"], "Direct Technical Instruction")