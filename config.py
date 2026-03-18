import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Resolve the path to the .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class AppConfig(BaseSettings):
    """
    Central configuration for Project Indigo.
    Values are automatically pulled from environment variables 
    or use the defaults provided here.
    """
    
    # --- API KEYS ---
    # These must be in your .env file
    GROQ_API_KEY: str = Field(default=...)
    TAVILY_API_KEY: str = Field(default=...)
    
    # --- MODEL SELECTIONS ---
    # Centralizing model names makes swapping them easy
    MODEL_LOGIC_HEAVY: str = "llama-3.3-70b-specdec"
    MODEL_FAST_SYNTHESIS: str = "llama-3.1-8b-instant"
    
    # --- GLOBAL SYSTEM CONSTANTS ---
    PASSING_SCORE: int = 80
    MAX_ATTEMPTS_PER_NODE: int = 3
    MAX_SYLLABUS_STEPS: int = 5
    
    # --- DIRECTORY PATHS ---
    BASE_DIR: Path = Path(__file__).parent.parent
    PROMPTS_DIR: Path = BASE_DIR / "prompts"
    
    # Pydantic Settings configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

# Instantiate as a singleton to be used across the app
_config = AppConfig()

def get_config() -> AppConfig:
    """Helper function to get the current configuration."""
    return _config