from app.agents.base_agent import BaseAgent


class EscalationAgent(BaseAgent):
    name = "escalation_agent"

    def can_handle(self, query: str) -> bool:
        return True

    def handle(self, query: str, context: dict = None) -> dict:
        return {
            "agent": self.name,
            "confidence": 0.6,
            "answer": "Your request has been escalated to a human agent. Expect a callback soon.",
            "reason": "Fallback escalation",
        }
