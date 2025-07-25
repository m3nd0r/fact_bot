"""High‑level APScheduler job implementation."""
from __future__ import annotations

from assistant import get_fact
from telegram import send_message, send_photo
from unsplash import get_image
from utils import format_fact_message, extract_title_en
from logger import logger


def daily_fact_job() -> None:
    """Fetch a fact and deliver it to Telegram once a day."""
    logger.info("Requesting fact from OpenAI Assistant …")
    fact = get_fact()
    if not fact:
        logger.error("Failed to retrieve fact. Aborting dispatch.")
        return

    image_url = None
    title_en = extract_title_en(fact)
    if title_en:
        image_url = get_image(title_en)

    message = format_fact_message(fact)
    if image_url:
        send_photo(image_url, message)
    else:
        send_message(message)
