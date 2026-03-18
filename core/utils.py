import yaml
import re
from pathlib import Path
from typing import Any, Dict
from config import get_config

def load_node_prompt(category: str, node_name: str) -> Dict[str, Any]:
    """
    Utility to fetch a specific node's prompt from the YAML directory.
    
    Args:
        category (str): The folder name (e.g., 'blueprint', 'learning', 'proof')
        node_name (str): The filename without extension (e.g., 'goal_setter')
    """
    config = get_config()
    
    # Construct path: project_indigo/prompts/{category}/{node_name}.yaml
    prompt_path = config.PROMPTS_DIR / category / f"{node_name}.yaml"
    
    if not prompt_path.exists():
        # Fallback to current directory if PROMPTS_DIR isn't set
        prompt_path = Path(__file__).parent.parent / "prompts" / category / f"{node_name}.yaml"
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found at: {prompt_path}")
        
    with open(prompt_path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML for {node_name}: {e}")

def format_prompt(template: str, **kwargs) -> str:
    """
    Helper to inject GraphState variables into YAML string templates.
    Uses a safe formatter to avoid crashes on code blocks (curly braces).
    """
    # Regex to find {variable_name} but ignore {{escaped_braces}}
    # This ensures code blocks in prompts don't break the formatter.
    def replace_match(match):
        key = match.group(1)
        return str(kwargs.get(key, f"<{key}_MISSING>"))

    try:
        # Replaces {key} with value from kwargs
        return re.sub(r'(?<!\{)\{([a-zA-Z0-9_]+)\}(?!\})', replace_match, template)
    except Exception as e:
        return f"FORMAT_ERROR: {str(e)}\n\nTemplate: {template[:100]}..."