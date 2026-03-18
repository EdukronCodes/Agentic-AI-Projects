import re
from app.agents.base_agent import BaseAgent


class AccountManagementAgent(BaseAgent):
    name = "account_management_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(account|profile|login|sign in|password|create account)\b", query))

    def handle(self, query: str, context: dict = None) -> dict:
        return {
            "agent": self.name,
            "confidence": 0.88,
            "answer": "You can update account settings in the profile section. For security changes, you may need to confirm via email.",
            "reason": "Account management request",
        }
