import re
from typing import Dict, Optional
from .base_agent import BaseAgent


class FAQAgent(BaseAgent):
    name = "faq_agent"
    prompt = "Answer common FAQ questions using the knowledge base first."

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(return policy|reset password|ship|shipping|faq|question)\b", query))

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        base = context.get("knowledge", "") if context else ""
        return {
            "agent": self.name,
            "confidence": 0.85,
            "answer": f"FAQ response with context: {base} \nYour question: {query}",
            "reason": "Matched FAQ keywords",
        }


class OrderStatusAgent(BaseAgent):
    name = "order_status_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(order status|track order|order #|shipping status|delivery)\b", query))

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        order_id = None
        match = re.search(r"\b(\d{4,})\b", query)
        if match:
            order_id = match.group(1)

        if context and "order" in context:
            order_state = context["order"]
            result = f"Order {order_id or order_state.get('order_id', 'unknown')} is currently {order_state.get('status', 'unknown')}"
        else:
            result = f"Order {order_id or '[unknown]'} is in transit. Please verify your order ID." if order_id else "Please provide your order ID."

        return {
            "agent": self.name,
            "confidence": 0.9,
            "answer": result,
            "reason": "Order-related keywords detected",
        }


class ReturnsRefundAgent(BaseAgent):
    name = "returns_refund_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(return|refund|exchange)\b", query))

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        return {
            "agent": self.name,
            "confidence": 0.87,
            "answer": "Our returns and refunds policy: 30 days, unopened products accepted. You can initiate a return from your account dashboard.",
            "reason": "Returns/refunds keywords detected",
        }


class TechnicalSupportAgent(BaseAgent):
    name = "technical_support_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(error|bug|issue|technical|crash|not working)\b", query))

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        return {
            "agent": self.name,
            "confidence": 0.88,
            "answer": "Please describe the issue in detail. Meanwhile try restarting the application and clearing browser cache.",
            "reason": "Technical support request",
        }


class BillingAgent(BaseAgent):
    name = "billing_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(bill|billing|invoice|charge|payment)\b", query))

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        return {
            "agent": self.name,
            "confidence": 0.85,
            "answer": "Billing: check invoices page for details. If unauthorized charge, contact support with transaction ID.",
            "reason": "Billing-related keywords",
        }


class AccountManagementAgent(BaseAgent):
    name = "account_management_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(account|profile|login|sign in|password|create account)\b", query))

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        return {
            "agent": self.name,
            "confidence": 0.88,
            "answer": "You can update account settings in the profile section. For security changes, you may need to confirm via email.",
            "reason": "Account management request",
        }


class ComplaintHandlingAgent(BaseAgent):
    name = "complaint_handling_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(complaint|issue|unsatisfied|bad experience|not happy)\b", query))

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        return {
            "agent": self.name,
            "confidence": 0.8,
            "answer": "We are sorry you faced issues. A customer relations specialist will contact you within 1 business day.",
            "reason": "Complaint handling",
        }


class EscalationAgent(BaseAgent):
    name = "escalation_agent"

    def can_handle(self, query: str) -> bool:
        return True

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        return {
            "agent": self.name,
            "confidence": 0.6,
            "answer": "Your request has been escalated to a human agent. Expect a callback soon.",
            "reason": "Fallback escalation",
        }


class FeedbackAgent(BaseAgent):
    name = "feedback_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(feedback|rate|review|suggestion)\b", query))

    def handle(self, query: str, context: Dict[str, str] = None) -> Dict[str, str]:
        return {
            "agent": self.name,
            "confidence": 0.8,
            "answer": "Thanks for your feedback! We have recorded your notes and will improve accordingly.",
            "reason": "Feedback submission",
        }


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
