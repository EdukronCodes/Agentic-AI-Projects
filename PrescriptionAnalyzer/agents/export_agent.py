from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base_agent import BaseAgent


class ExportAgent(BaseAgent):
    """Exports prescription analysis results to JSON for downstream consumption."""

    def run(self, prescription_text: str, output_path: str | Path = "analysis_output.json") -> str:
        # This agent doesn't call the LLM; it just formats the output.
        result = {
            "prescription_text": prescription_text,
            "analysis": {
                "summary": "",
                "dosage": "",
                "side_effects": "",
                "interactions": "",
                "compliance": "",
                "regulatory": "",
            },
        }

        output_path = Path(output_path)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        return f"Exported analysis to {output_path.absolute()}"
