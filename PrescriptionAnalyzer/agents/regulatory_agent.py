from .base_agent import BaseAgent


class RegulatoryAgent(BaseAgent):
    """Highlights regulatory or safety warnings based on prescription content."""

    def run(self, prescription_text: str) -> str:
        template = (
            "You are a regulatory compliance assistant. "
            "Review the prescription and identify any regulatory or safety warnings that should be highlighted (e.g., contraindications, monitoring requirements, restricted medications). "
            "If none are identified, respond with 'No regulatory warnings identified.'\n\n"
            "Prescription:\n{prescription_text}\n\nRegulatory warnings:")
        chain = self._chain(template)
        return chain.run(prescription_text=prescription_text)
