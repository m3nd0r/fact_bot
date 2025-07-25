"""Centralised configuration loaded from the environment (.env)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application settings read once at startup."""

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ASSISTANT_ID: str = os.getenv("ASSISTANT_ID", "")
    AGENT_PROMPT: str = os.getenv("AGENT_PROMPT", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    UNSPLASH_API_KEY: str = os.getenv("UNSPLASH_API_KEY", "")
    SEND_TIME_HOUR: int = int(os.getenv("SEND_TIME_HOUR", "13"))
    SEND_TIME_MINUTE: int = int(os.getenv("SEND_TIME_MINUTE", "0"))


settings = Settings()
