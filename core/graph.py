"""Graph utilities and orchestration."""
from typing import Any, Dict, List


class Graph:
    def __init__(self):
        self.nodes: Dict[str, Any] = {}

    def add(self, name: str, node: Any):
        self.nodes[name] = node

    def run(self):
        # placeholder for orchestration logic
        return {k: getattr(v, "run", lambda: None)() for k, v in self.nodes.items()}
