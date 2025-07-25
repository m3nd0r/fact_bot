"""All OpenAI Assistant interaction logic lives here."""
from __future__ import annotations

import json
import time
from typing import Optional, Dict, Any

import openai

from config import settings
from logger import logger

openai.api_key = settings.OPENAI_API_KEY


def get_fact() -> Optional[Dict[str, Any]]:
    """
    Request an interesting fact from the OpenAI Assistant and return it as a dictionary.
    Important: the assistant should be prepared to respond to the prompt in the `.env` file.

    The assistant is expected to respond with a JSON string like
    `{ "title": "…", "fact": "…", "title_en": "…" }`.

    Returns
    -------
    Optional[Dict[str, Any]]
        The parsed dictionary or ``None`` if something went wrong.
    """
    thread = openai.beta.threads.create()

    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=settings.AGENT_PROMPT,
    )
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=settings.ASSISTANT_ID,
    )

    # Poll until the assistant has finished processing
    while True:
        status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if status.status == "completed":
            break
        time.sleep(1)

    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    for message in messages.data:
        if message.role == "assistant":
            raw = message.content[0].text.value
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                logger.error("Failed to parse assistant response as JSON. Raw: %s", raw)
                return None
    logger.error("Assistant response not found in thread messages.")
    return None
