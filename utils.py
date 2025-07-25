"""Pure utility helpers (string formatting & parsing)."""
from typing import Dict, Any, Optional


def format_fact_message(fact: Dict[str, Any]) -> str:
    """Return an HTML‑formatted fact message suitable for Telegram."""
    title = fact.get("title", "").strip()
    fact_text = fact.get("fact", "").strip()
    return f"<b>{title}</b>\n\n{fact_text}"


def extract_title_en(fact: Dict[str, Any]) -> Optional[str]:
    """Extract the English title from fact if present and of the correct type."""
    value = fact.get("title_en")
    return value if isinstance(value, str) else None
