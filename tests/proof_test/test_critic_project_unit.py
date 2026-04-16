import unittest
from unittest.mock import MagicMock, patch
from nodes.proof.critic_project import critic_project_node

class TestCriticProjectNode(unittest.TestCase):

    def setUp(self):
        # Mock a syllabus with 3 topics
        self.topic_0 = MagicMock(title="Topic 0")
        self.topic_1 = MagicMock(title="Topic 1")
        self.topic_2 = MagicMock(title="Topic 2")
        
        self.state = {
            "user_input": "print('hello')", # Simulated submission
            "grading_rubric": "Must use LangGraph StateGraph.",
            "syllabus": [self.topic_0, self.topic_1, self.topic_2],
            "history_summary": "User completed all lessons."
        }

    @patch('nodes.proof.critic_project.get_model')
    @patch('nodes.proof.critic_project.load_node_prompt')
    def test_critic_failure_recovery(self, mock_load, mock_model):
        mock_load.return_value = {"system_prompt": "You are a code auditor."}
        
        # Mock a FAILURE audit (Score 60)
        mock_audit = MagicMock()
        mock_audit.score = 60
        mock_audit.failed_subtopic_indices = [1] # Failed ONLY the second topic
        mock_audit.failure_critique = "Missing edge logic."
        
        mock_llm = mock_model.return_value
        mock_llm.with_structured_output.return_value.invoke.return_value = mock_audit

        # Run Node
        result = critic_project_node(self.state)

        # Assertions
        self.assertFalse(result["is_complete"])
        self.assertFalse(result["is_approved"])
        # CRITICAL: Verify the syllabus was pruned to ONLY the failed topic
        self.assertEqual(len(result["syllabus"]), 1)
        self.assertEqual(result["syllabus"][0].title, "Topic 1")
        self.assertEqual(result["current_topic_index"], 0)