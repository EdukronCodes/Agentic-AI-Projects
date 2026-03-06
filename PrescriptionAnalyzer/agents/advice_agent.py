from .base_agent import BaseAgent


class AdviceAgent(BaseAgent):
    """Provides patient-facing advice based on a prescription."""

    def run(self, prescription_text: str) -> str:
        template = (
            "You are a patient-facing medication advisor. "
            "Read the following prescription and provide clear, concise advice to a patient about how to take the medication, including what to do if a dose is missed. "
            "Do not provide medical advice beyond general guidelines.\n\n"
            "Prescription:\n{prescription_text}\n\nPatient advice:")
        chain = self._chain(template)
        return chain.run(prescription_text=prescription_text)
