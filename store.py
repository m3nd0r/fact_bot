from __future__ import annotations

from typing import Optional

import redis.asyncio as redis

from config import settings

_redis = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_thread_id(tg_id: int) -> Optional[str]:
    return await _redis.get(f"thread:{tg_id}")


async def set_thread_id(tg_id: int, thread_id: str) -> None:
    await _redis.set(f"thread:{tg_id}", thread_id)
