from .base_agent import BaseAgent


class ComplianceAgent(BaseAgent):
    """Checks for adherence to typical prescription compliance guidelines."""

    def run(self, prescription_text: str) -> str:
        template = (
            "You are a medication compliance analyst. "
            "Evaluate the following prescription for potential compliance issues (e.g., unclear instructions, missing patient information, ambiguous dosage). "
            "List any issues found or respond with 'No compliance issues identified.'\n\n"
            "Prescription:\n{prescription_text}\n\nCompliance analysis:")
        chain = self._chain(template)
        return chain.run(prescription_text=prescription_text)
