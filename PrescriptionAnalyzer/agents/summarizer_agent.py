from .base_agent import BaseAgent


class SummarizerAgent(BaseAgent):
    """Produces a short summary of a prescription text."""

    def run(self, prescription_text: str) -> str:
        template = (
            "You are a medical document assistant. "
            "Given the following prescription text, provide a concise summary that highlights the key medication names, dosages, and instructions.\n\n" 
            "Prescription:\n{prescription_text}\n\nSummary:")
        chain = self._chain(template)
        return chain.run(prescription_text=prescription_text)
