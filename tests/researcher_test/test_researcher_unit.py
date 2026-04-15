import unittest
from unittest.mock import MagicMock, patch
from nodes.blueprint.researcher import researcher_node

class TestResearcherNode(unittest.TestCase):

    def setUp(self):
        self.state = {
            "terminal_objective": "Build a LangGraph agent with Groq Llama3."
        }

    @patch('nodes.blueprint.researcher.TavilyClient')
    @patch('nodes.blueprint.researcher.get_model')
    @patch('nodes.blueprint.researcher.load_node_prompt')
    def test_research_success(self, mock_load, mock_model, mock_tavily):
        # 1. Setup Mocks
        mock_load.return_value = {"system_prompt": "test"}
        
        # Simulate LLM generating 3 queries
        mock_response = MagicMock()
        mock_response.content = "LangGraph architecture\nGroq Llama3 API\nLangGraph examples"
        mock_model.return_value.invoke.return_value = mock_response
        
        # Simulate Tavily returning results
        mock_tavily_instance = mock_tavily.return_value
        mock_tavily_instance.search.return_value = {
            "results": [
                {"url": "https://test.com", "content": "LangGraph is a library..."}
            ]
        }

        # 2. Run Node
        result = researcher_node(self.state)

        # 3. Assertions
        self.assertIn("source_material", result)
        self.assertEqual(len(result["source_material"]), 3)
        self.assertIn("Research complete", result["history_summary"])
        

    @patch('nodes.blueprint.researcher.TavilyClient')
    def test_knowledge_gap(self, mock_tavily):
        # Simulate Tavily returning zero results
        mock_tavily_instance = mock_tavily.return_value
        mock_tavily_instance.search.return_value = {"results": []}
        
        # We need to mock the LLM too or it will crash during query gen
        with patch('nodes.blueprint.researcher.get_model') as mock_model:
            mock_model.return_value.invoke.return_value = MagicMock(content="q1\nq2\nq3")
            result = researcher_node(self.state)

        self.assertFalse(result["is_approved"])
        self.assertEqual(result["source_material"], [])