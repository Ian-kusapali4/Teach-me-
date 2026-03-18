"""Simple configuration loader."""
from pathlib import Path
import os

def _load_env():
    env_path = Path(__file__).parent / ".env"
    result = {}
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                result[k.strip()] = v.strip()
    return result

settings = _load_env()
