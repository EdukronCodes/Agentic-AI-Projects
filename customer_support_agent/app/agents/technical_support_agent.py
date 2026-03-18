import re
from app.agents.base_agent import BaseAgent


class TechnicalSupportAgent(BaseAgent):
    name = "technical_support_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(error|bug|issue|technical|crash|not working)\b", query))

    def handle(self, query: str, context: dict = None) -> dict:
        return {
            "agent": self.name,
            "confidence": 0.88,
            "answer": "Please describe the issue in detail. Meanwhile try restarting the application and clearing browser cache.",
            "reason": "Technical support request",
        }
