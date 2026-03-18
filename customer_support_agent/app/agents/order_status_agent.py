import re
from app.agents.base_agent import BaseAgent


class OrderStatusAgent(BaseAgent):
    name = "order_status_agent"

    def can_handle(self, query: str) -> bool:
        return bool(re.search(r"(?i)\b(order status|track order|order #|shipping status|delivery)\b", query))

    def handle(self, query: str, context: dict = None) -> dict:
        order_id = None
        match = re.search(r"\b(\d{4,})\b", query)
        if match:
            order_id = match.group(1)

        if context and isinstance(context, dict) and context.get("order"):
            order_state = context["order"]
            result = f"Order {order_id or order_state.get('order_id', 'unknown')} is currently {order_state.get('status', 'unknown')}"
        else:
            if order_id:
                result = f"Order {order_id} is in transit. Please verify your order ID."
            else:
                result = "Please provide your order ID."

        return {
            "agent": self.name,
            "confidence": 0.9,
            "answer": result,
            "reason": "Order-related keywords detected",
        }
