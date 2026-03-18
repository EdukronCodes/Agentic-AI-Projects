import re
from app.agents.base_agent import BaseAgent


class BillingAgent(BaseAgent):
    name = "billing_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(bill|billing|invoice|charge|payment)\b", query))

    def handle(self, query: str, context: dict = None) -> dict:
        return {
            "agent": self.name,
            "confidence": 0.85,
            "answer": "Billing: check invoices page for details. If unauthorized charge, contact support with transaction ID.",
            "reason": "Billing-related keywords",
        }
