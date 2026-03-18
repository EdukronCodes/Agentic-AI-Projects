import re
from app.agents.base_agent import BaseAgent


class ComplaintHandlingAgent(BaseAgent):
    name = "complaint_handling_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(complaint|issue|unsatisfied|bad experience|not happy)\b", query))

    def handle(self, query: str, context: dict = None) -> dict:
        return {
            "agent": self.name,
            "confidence": 0.8,
            "answer": "We are sorry you faced issues. A customer relations specialist will contact you within 1 business day.",
            "reason": "Complaint handling",
        }
