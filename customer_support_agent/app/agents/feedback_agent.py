import re
from app.agents.base_agent import BaseAgent


class FeedbackAgent(BaseAgent):
    name = "feedback_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(feedback|rate|review|suggestion)\b", query))

    def handle(self, query: str, context: dict = None) -> dict:
        return {
            "agent": self.name,
            "confidence": 0.8,
            "answer": "Thanks for your feedback! We have recorded your notes and will improve accordingly.",
            "reason": "Feedback submission",
        }
