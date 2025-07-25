"""Unsplash API wrapper."""
from __future__ import annotations

from typing import Optional

import requests

from config import settings
from logger import logger


UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"


def get_image(query: str) -> Optional[str]:
    """
    Return the URL of the first Unsplash image matching *query* or ``None``.

    We only need a single popular landscape photo as a background for the fact card.

    Parameters
    ----------
    query : str
        The query to search for.

    Returns
    -------
    Optional[str]
        The URL of the first Unsplash image matching *query* or ``None``.
    """
    params = {
        "query": query,
        "client_id": settings.UNSPLASH_API_KEY,
        "order_by": "popular",
        "orientation": "landscape",
    }
    try:
        response = requests.get(UNSPLASH_SEARCH_URL, params=params, timeout=15)
    except requests.RequestException as exc:
        logger.error("Unsplash request failed: %s", exc)
        return None

    if response.ok:
        data = response.json()
        if data.get("results"):
            return data["results"][0]["urls"]["regular"]
    logger.warning("Unsplash returned no results for query: '%s'", query)
    return None
