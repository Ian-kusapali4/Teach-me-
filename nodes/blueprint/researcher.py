import datetime
from typing import Dict, Any, List
from tavily import TavilyClient
from core.models import get_model
from core.utils import load_node_prompt, format_prompt
from core.schemas import GraphState
from config import get_config

def researcher_node(state: GraphState) -> Dict[str, Any]:
    """
    Implementation of the Weighted Retrieval Researcher.
    Uses Tavily to fetch, filter, and prune web data into Atomic Snippets.
    """
    config = get_config()
    tavily = TavilyClient(api_key=config.TAVILY_API_KEY)
    
    # 1. SETUP: Load Research Persona
    prompt_data = load_node_prompt("blueprint", "researcher")
    llm = get_model("researcher")
    
    # 2. BRANCH: Multi-Query Generation
    # We ask the LLM to generate the 3 specific queries (Architecture, Code, Errors)
    formatted_prompt = format_prompt(
        prompt_data["system_prompt"], 
        terminal_objective=state.get("terminal_objective")
    )
    
    # The LLM returns a list of 3 strings based on our YAML template
    query_response = llm.invoke(formatted_prompt)
    queries = [q.strip() for q in query_response.content.split("\n") if q.strip()][:3]

    # 3. FETCH & FILTER (Weighted Retrieval)
    all_snippets = []
    current_year = datetime.datetime.now().year
    
    for query in queries:
        # We use Tavily's 'advanced' search to get full page content (Step 5: Scrape)
        search_result = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=3,
            include_raw_content=True
        )
        
        for res in search_result.get("results", []):
            # Step 4: Recency Filter (Basic URL/Content check)
            # Tavily often provides 'published_date' if available
            all_snippets.append({
                "url": res.get("url"),
                "content": res.get("content")[:1500] # Step 7: Context Budgeting
            })

    # 4. VALIDATE (Knowledge Gap Check)
    if not all_snippets:
        return {
            "is_approved": False,
            "last_critique": "Knowledge Gap Detected: I couldn't find authoritative data for this topic. Let's re-scope.",
            "source_material": []
        }

    # 5. INJECT (State Update)
    # We take the top 5 most relevant snippets as per your logic
    final_material = all_snippets[:5]
    
    print(f"--- [RESEARCHER] Found {len(final_material)} authoritative sources. ---")

    return {
        "source_material": final_material,
        "history_summary": f"Research complete. Found {len(final_material)} snippets."
    }

# 5. INJECT (State Update)
# TODO: Implement a Reranker or Domain Filter here.for example Filter by 'langchain.com' or 'github.com' domain priority.
#final_material = all_snippets[:5]
#critic node to evaluate the relevance of the snippets and potentially loop back to researcher for more focused queries if the material does not give a clear path of learing eg a step by step guide.