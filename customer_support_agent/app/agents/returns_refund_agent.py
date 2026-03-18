import re
from app.agents.base_agent import BaseAgent


class ReturnsRefundAgent(BaseAgent):
    name = "returns_refund_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(return|refund|exchange)\b", query))

    def handle(self, query: str, context: dict = None) -> dict:
        return {
            "agent": self.name,
            "confidence": 0.87,
            "answer": "Our returns and refunds policy: 30 days, unopened products accepted. You can initiate a return from your account dashboard.",
            "reason": "Returns/refunds keywords detected",
        }
