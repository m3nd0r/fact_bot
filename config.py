"""Centralised configuration loaded from the environment (.env)."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _parse_id_to_name_mapping(env_value: str | None) -> dict[int, str]:
    """Parse ID_TO_NAME from environment variable format: 'user_id:Name,user_id:Name'."""
    if not env_value:
        return {}

    result = {}
    for pair in env_value.split(","):
        pair = pair.strip()
        if not pair or ":" not in pair:
            continue
        try:
            user_id_str, name = pair.split(":", 1)
            result[int(user_id_str)] = name
        except (ValueError, IndexError):
            # Skip malformed pairs
            continue

    return result


@dataclass(frozen=True)
class Settings:
    """Application settings read once at startup."""

    # API keys / tokens
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ASSISTANT_ID: str = os.getenv("ASSISTANT_ID", "")
    AGENT_PROMPT: str = os.getenv("AGENT_PROMPT", "")
    LISTENER_ASSISTANT_ID: str = os.getenv("LISTENER_ASSISTANT_ID", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    UNSPLASH_API_KEY: str = os.getenv("UNSPLASH_API_KEY", "")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    # Fact‑of‑the‑day schedule (HH:MM)
    SEND_TIME_HOUR: int = int(os.getenv("SEND_TIME_HOUR", "13"))
    SEND_TIME_MINUTE: int = int(os.getenv("SEND_TIME_MINUTE", "0"))

    # Triggers for the listener
    LISTENER_TRIGGERS: set[str] = (
        set(os.getenv("LISTENER_TRIGGERS", "").split(",")) if os.getenv("LISTENER_TRIGGERS") else set()
    )  # noqa: E501

    # User ID to custom name mapping (parsed from "user_id:Name,user_id:Name")
    ID_TO_NAME: dict[int, str] = _parse_id_to_name_mapping(os.getenv("ID_TO_NAME"))


settings = Settings()
