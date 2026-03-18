import yaml
from pathlib import Path
from typing import Any, Dict
from config import get_config

def load_node_prompt(category: str, node_name: str) -> Dict[str, Any]:
    """
    Utility to fetch a specific node's prompt from the YAML directory.
    
    Args:
        category (str): The folder name (e.g., 'blueprint', 'learning', 'proof')
        node_name (str): The filename without extension (e.g., 'goal_setter')
        
    Returns:
        Dict: The parsed YAML content (system_prompt, user_template, etc.)
    """
    config = get_config()
    
    # Construct path: project_indigo/prompts/{category}/{node_name}.yaml
    prompt_path = config.PROMPTS_DIR / category / f"{node_name}.yaml"
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found at: {prompt_path}")
        
    with open(prompt_path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML for {node_name}: {e}")

def format_prompt(template: str, **kwargs) -> str:
    """
    Helper to inject GraphState variables into the YAML string templates.
    Handles missing keys gracefully.
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        # Fallback if a variable is missing in the state
        return f"MISSING_DATA: {e}\n\nOriginal Template: {template}"