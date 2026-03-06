from __future__ import annotations

from typing import Any

from langchain import OpenAI, LLMChain, PromptTemplate

from ..config import settings


class BaseAgent:
    """Base class for all prescription analysis agents."""

    def __init__(self, llm: OpenAI | None = None):
        self.llm = llm or OpenAI(
            model_name=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY,
        )

    def run(self, prescription_text: str, **kwargs: Any) -> str:
        raise NotImplementedError("Agents must implement run().")

    def _chain(self, template: str) -> LLMChain:
        prompt = PromptTemplate(input_variables=["prescription_text"], template=template)
        return LLMChain(llm=self.llm, prompt=prompt)
