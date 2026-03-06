"""Agent registry for the Prescription Analyzer project."""

from .advice_agent import AdviceAgent
from .classification_agent import ClassificationAgent
from .compliance_agent import ComplianceAgent
from .counterfeit_agent import CounterfeitAgent
from .dosage_agent import DosageAgent
from .export_agent import ExportAgent
from .interactions_agent import InteractionsAgent
from .regulatory_agent import RegulatoryAgent
from .side_effects_agent import SideEffectsAgent
from .summarizer_agent import SummarizerAgent


AGENT_REGISTRY = {
    "summarize": SummarizerAgent,
    "dosage": DosageAgent,
    "side_effects": SideEffectsAgent,
    "interactions": InteractionsAgent,
    "compliance": ComplianceAgent,
    "counterfeit": CounterfeitAgent,
    "classification": ClassificationAgent,
    "regulatory": RegulatoryAgent,
    "advice": AdviceAgent,
    "export": ExportAgent,
}


def get_agent(name: str):
    """Return an agent class for a given name."""
    return AGENT_REGISTRY.get(name)
