from typing import Dict, Optional
from app.agents.base_agent import BaseAgent


class RouterAgent(BaseAgent):
    name = "router_agent"

    def __init__(self, agents: Optional[Dict[str, BaseAgent]] = None):
        self.agents = agents or {}

    def can_handle(self, query: str) -> bool:
        return True

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        for agent in self.agents.values():
            if agent.name != self.name and agent.can_handle(query):
                return {
                    "agent": self.name,
                    "match": agent.name,
                    "confidence": 1.0,
                    "reason": f"Routed to {agent.name}",
                }

        return {
            "agent": self.name,
            "match": "escalation_agent",
            "confidence": 0.5,
            "reason": "No match found, fallback",
        }
