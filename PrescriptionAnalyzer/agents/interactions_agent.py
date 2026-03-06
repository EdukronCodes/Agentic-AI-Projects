from .base_agent import BaseAgent


class InteractionsAgent(BaseAgent):
    """Identifies possible drug-drug interactions from a prescription."""

    def run(self, prescription_text: str) -> str:
        template = (
            "You are a clinical pharmacist assistant. "
            "Analyze the prescription below and list any possible drug-drug interactions, including the interacting drugs and the nature of the interaction. "
            "If none are found, respond with 'No interactions detected.'\n\n"
            "Prescription:\n{prescription_text}\n\nInteractions:")
        chain = self._chain(template)
        return chain.run(prescription_text=prescription_text)
