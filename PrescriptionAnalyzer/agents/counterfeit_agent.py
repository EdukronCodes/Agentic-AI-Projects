from .base_agent import BaseAgent


class CounterfeitAgent(BaseAgent):
    """Looks for signs that a prescription might be fraudulent or counterfeit."""

    def run(self, prescription_text: str) -> str:
        template = (
            "You are a fraud detection assistant for prescription documents. "
            "Analyze the text below and list indicators that the prescription may be fraudulent, forged, or otherwise suspicious. "
            "If it appears genuine, respond with 'No suspicious indicators found.'\n\n"
            "Prescription:\n{prescription_text}\n\nFraud analysis:")
        chain = self._chain(template)
        return chain.run(prescription_text=prescription_text)
