from typing import Dict


class BaseAgent:
    """Base class for agents with simple structured response format."""

    name = "base"

    def __init__(self):
        pass

    def can_handle(self, query: str) -> bool:
        """Check whether agent is a candidate for a query using keyword matching."""
        raise NotImplementedError

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        """Handle user query and return structured output."""
        raise NotImplementedError
