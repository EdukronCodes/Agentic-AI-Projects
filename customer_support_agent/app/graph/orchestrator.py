from typing import Dict, List, Optional

# LangGraph is optional; with a fallback graph model running without the package.
try:
    from langgraph import Graph, Node
except ImportError:
    Graph = None
    Node = None

from app.agents import (
    AccountManagementAgent,
    BillingAgent,
    ComplaintHandlingAgent,
    EscalationAgent,
    FAQAgent,
    FeedbackAgent,
    OrderStatusAgent,
    ReturnsRefundAgent,
    RouterAgent,
    TechnicalSupportAgent,
)
from app.rag.rag_pipeline import RAGPipeline


class LangGraphOrchestrator:
    """Simple LangGraph-style orchestrator with routing, fallback, and memory."""

    def __init__(self, rag_pipeline: Optional[RAGPipeline] = None):
        self.rag = rag_pipeline or RAGPipeline()
        self.agents = {
            "faq_agent": FAQAgent(),
            "order_status_agent": OrderStatusAgent(),
            "returns_refund_agent": ReturnsRefundAgent(),
            "technical_support_agent": TechnicalSupportAgent(),
            "billing_agent": BillingAgent(),
            "account_management_agent": AccountManagementAgent(),
            "complaint_handling_agent": ComplaintHandlingAgent(),
            "escalation_agent": EscalationAgent(),
            "feedback_agent": FeedbackAgent(),
        }
        self.router = RouterAgent(self.agents)
        self.history: List[Dict] = []
        self._build_graph()

    def _build_graph(self):
        try:
            self.graph = Graph("customer_support_graph")
            router_node = Node("router")
            self.graph.add_node(router_node)
            for agent_name in self.agents.keys():
                agent_node = Node(agent_name)
                self.graph.add_node(agent_node)
                self.graph.add_edge(router_node, agent_node)
            response_node = Node("response")
            self.graph.add_node(response_node)
            for agent_name in self.agents.keys():
                agent_node = self.graph.get_node(agent_name)
                self.graph.add_edge(agent_node, response_node)
        except Exception:
            self.graph = None

    def run(self, query: str) -> Dict:
        route = self.router.handle(query)
        target_agent_name = route.get("match") or "escalation_agent"

        if target_agent_name not in self.agents:
            target_agent_name = "escalation_agent"

        context_data = {
            "knowledge": self.rag.retrieve_context(query),
            "query": query,
        }

        agent = self.agents[target_agent_name]
        try:
            result = agent.handle(query, context_data)
        except Exception as exc:
            agent = self.agents["escalation_agent"]
            result = agent.handle(query, context_data)
            result["fallback_reason"] = str(exc)

        entry = {
            "query": query,
            "selected_agent": target_agent_name,
            "router": route,
            "context": context_data,
            "result": result,
        }

        self.history.append(entry)
        if len(self.history) > 50:
            self.history.pop(0)

        return entry

    def get_chat_history(self) -> List[Dict]:
        return self.history
