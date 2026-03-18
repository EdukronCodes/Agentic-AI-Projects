import re
from app.agents.base_agent import BaseAgent


class FAQAgent(BaseAgent):
    name = "faq_agent"
    prompt = "Answer common FAQ questions using the knowledge base first."

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(return policy|reset password|ship|shipping|faq|question)\b", query))

    def handle(self, query: str, context: dict = None) -> dict:
        base = context.get("knowledge", "") if context else ""
        return {
            "agent": self.name,
            "confidence": 0.85,
            "answer": f"FAQ response with context: {base} \nYour question: {query}",
            "reason": "Matched FAQ keywords",
        }
