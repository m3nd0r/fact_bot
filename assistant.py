"""All OpenAI Assistant interaction logic lives here."""

from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, Optional, Tuple

import openai

from config import settings
from logger import logger

openai.api_key = settings.OPENAI_API_KEY


async def run_assistant_async(
    assistant_id: str,
    prompt: str,
    *,
    thread_id: str | None = None,
) -> Tuple[str, str]:
    """
    Send prompt to assistant_id and return (reply, thread_id).

    If thread_id is None a new thread is created. The caller can persist
    the returned thread_id to keep memory between messages.
    """

    if thread_id is None:
        thread_obj = await asyncio.to_thread(openai.beta.threads.create)
        thread_id = thread_obj.id
        logger.debug("Created new thread %s for assistant %s", thread_id, assistant_id)

    # Add user message
    await asyncio.to_thread(
        openai.beta.threads.messages.create,
        thread_id=thread_id,
        role="user",
        content=prompt,
    )

    # Run the assistant
    run = await asyncio.to_thread(
        openai.beta.threads.runs.create,
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    # Wait for completion
    while True:
        status = await asyncio.to_thread(
            openai.beta.threads.runs.retrieve,
            thread_id=thread_id,
            run_id=run.id,
        )
        if status.status == "completed":
            break
        await asyncio.sleep(1)

    # Extract assistant reply
    messages = await asyncio.to_thread(openai.beta.threads.messages.list, thread_id=thread_id)
    for msg in messages.data:
        if msg.role == "assistant":
            return msg.content[0].text.value.strip(), thread_id

    logger.error("Assistant produced no reply in thread %s", thread_id)
    return "(no reply)", thread_id


def run_assistant(
    assistant_id: str,
    prompt: str,
    *,
    thread_id: Optional[str] = None,
) -> Tuple[str, str]:
    """Synchronous wrapper around run_assistant_async."""
    return asyncio.run(
        run_assistant_async(
            assistant_id=assistant_id,
            prompt=prompt,
            thread_id=thread_id,
        )
    )


def get_fact() -> Optional[Dict[str, Any]]:
    """Return JSON dict with daily fact using settings.ASSISTANT_ID."""
    text, _ = run_assistant(settings.ASSISTANT_ID, settings.AGENT_PROMPT)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logger.error("Failed to parse assistant daily fact JSON: %s", text)
        return None
