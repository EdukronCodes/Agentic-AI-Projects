from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    OPENAI_API_KEY: str | None = None
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
