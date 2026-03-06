from .base_agent import BaseAgent


class ClassificationAgent(BaseAgent):
    """Classifies the prescription into common categories (e.g., acute, chronic, controlled substance)."""

    def run(self, prescription_text: str) -> str:
        template = (
            "You are a clinical classification assistant. "
            "Classify the prescription below into one or more of the following categories: acute, chronic, controlled substance, outpatient, inpatient, OTC, or other. "
            "Provide a short explanation for each assigned category.\n\n"
            "Prescription:\n{prescription_text}\n\nClassification:")
        chain = self._chain(template)
        return chain.run(prescription_text=prescription_text)
