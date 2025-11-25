from __future__ import annotations

import asyncio
import signal
from typing import Final

from openai import beta as oai_beta
from telegram import Update, User
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from assistant import run_assistant_async
from config import settings
from logger import logger
from store import get_thread_id, set_thread_id

TRIGGERS: Final[set[str]] = settings.LISTENER_TRIGGERS  # "bot" is a trigger word for the bot
ID_TO_NAME: Final[dict[int, str]] = settings.ID_TO_NAME
_initialized: set[str] = set()


async def _ensure_thread(user: User) -> str:
    """Return thread_id for user, creating one with a system intro if needed."""

    if thread_id := await get_thread_id(user.id):
        return thread_id

    thread = await asyncio.to_thread(oai_beta.threads.create)
    await set_thread_id(user.id, thread.id)

    name = ID_TO_NAME.get(user.id, user.first_name or user.username or "user")

    intro = f"All messages in this thread are written by {name}. Address him exactly as such."
    await asyncio.to_thread(
        oai_beta.threads.messages.create,
        thread_id=thread.id,
        role="assistant",
        content=intro,
    )
    _initialized.add(thread.id)
    logger.info("New thread %s initialised for %s", thread.id, name)
    return thread.id


def _is_trigger(msg: Update.message, bot_id: int, bot_username: str) -> bool:
    """
    Return True if the bot is explicitly addressed.
    Here is a place to adjust the triggers.
    """

    text = (msg.text or "").casefold()
    by_word = any(tok in text for tok in TRIGGERS)
    by_mention = f"@{bot_username.casefold()}" in text
    by_reply = msg.reply_to_message and msg.reply_to_message.from_user and msg.reply_to_message.from_user.id == bot_id
    return by_word or by_mention or by_reply


async def _ask(user: User, prompt: str) -> str:
    thread_id = await _ensure_thread(user)

    reply, _ = await run_assistant_async(settings.LISTENER_ASSISTANT_ID, prompt, thread_id=thread_id)
    return reply


async def _on_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """React only to trigger words in the configured chat."""

    msg = update.effective_message
    if not msg or msg.chat_id != int(settings.TELEGRAM_CHAT_ID):
        return

    if not _is_trigger(msg, ctx.bot.id, ctx.bot.username):
        return

    reply = await _ask(msg.from_user, msg.text or "")
    await msg.reply_text(reply, parse_mode="HTML")


def _build_app() -> Application:
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _on_message))
    return app


def _start_polling(app: Application) -> None:
    """Start the bot depending on whether an event loop already runs."""

    try:
        # Running inside uv/Jupyter?
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Normal CLI mode: this call blocks until SIGINT/SIGTERM
        app.run_polling(stop_signals=(signal.SIGINT, signal.SIGTERM))
    else:
        # Non-blocking start inside existing loop
        loop.create_task(app.initialize())
        loop.create_task(app.start())
        logger.info("Listener started inside existing loop %s", loop)


def main() -> None:
    if not settings.LISTENER_ASSISTANT_ID:
        raise RuntimeError("LISTENER_ASSISTANT_ID is not set in environment")

    logger.info("Starting mention listener (Assistant %s)…", settings.LISTENER_ASSISTANT_ID)
    _start_polling(_build_app())


if __name__ == "__main__":
    main()
