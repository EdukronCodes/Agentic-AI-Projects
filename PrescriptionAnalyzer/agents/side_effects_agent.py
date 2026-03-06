from .base_agent import BaseAgent


class SideEffectsAgent(BaseAgent):
    """Identifies potential side effects mentioned or implied in a prescription."""

    def run(self, prescription_text: str) -> str:
        template = (
            "You are a healthcare assistant. "
            "Read the prescription below and list any potential side effects that may be associated with the medication(s) prescribed. "
            "If no side effects are mentioned or implied, say 'No side effects identified.'\n\n"
            "Prescription:\n{prescription_text}\n\nPotential side effects:")
        chain = self._chain(template)
        return chain.run(prescription_text=prescription_text)
