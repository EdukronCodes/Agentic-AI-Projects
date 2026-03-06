from .base_agent import BaseAgent


class DosageAgent(BaseAgent):
    """Extracts dosage instructions from a prescription text."""

    def run(self, prescription_text: str) -> str:
        template = (
            "You are a medical data extraction assistant. "
            "Extract the dosage information (amount, frequency, route) from the following prescription text. "
            "If information is missing, say so.\n\n"
            "Prescription:\n{prescription_text}\n\nDosage information:")
        chain = self._chain(template)
        return chain.run(prescription_text=prescription_text)
