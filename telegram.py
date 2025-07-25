"""Telegram‑related helper functions."""
from __future__ import annotations

import requests

from config import settings
from logger import logger

API_ROOT = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"


def post_request(method: str, payload: dict) -> bool:
    """Send a JSON POST request to the Telegram Bot API.

    Parameters
    ----------
    method : str
        API method name, e.g. ``"sendMessage"``.
    payload : dict
        Parameters to be JSON‑encoded in the request body.

    Returns
    -------
    bool
        ``True`` if the request succeeded (``2xx`` status code), otherwise ``False``.
    """
    url = f"{API_ROOT}/{method}"
    try:
        response = requests.post(url, json=payload, timeout=15)
    except requests.RequestException as exc:
        logger.error("Telegram API request failed (%s): %s", method, exc)
        return False

    if response.ok:
        return True
    logger.error("Telegram API error (%s): %s", method, response.text)
    return False


def send_message(text: str) -> None:
    """Send a plain text message (HTML parse mode) to the configured chat."""
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    if post_request("sendMessage", payload):
        logger.info("Message sent to Telegram chat %s", settings.TELEGRAM_CHAT_ID)


def send_photo(photo_url: str, caption: str) -> None:
    """Send a photo with a caption (HTML parse mode) to the configured chat."""
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "HTML",
    }
    if post_request("sendPhoto", payload):
        logger.info("Photo sent to Telegram chat %s", settings.TELEGRAM_CHAT_ID)
