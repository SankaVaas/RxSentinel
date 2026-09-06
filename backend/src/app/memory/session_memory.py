"""Redis-backed short-term agent memory, scoped to a single agent run.

Used to cache intermediate retrieval/tool results within a run so that if
the graph is resumed after a transient failure, expensive lookups (RxNorm,
literature retrieval) aren't repeated.
"""
import json
import logging

import redis.asyncio as redis

from app.config import get_settings

logger = logging.getLogger(__name__)

_TTL_SECONDS = 60 * 30  # a single agent run should never take 30 minutes


class SessionMemory:
    def __init__(self, agent_run_id: str):
        settings = get_settings()
        self._redis = redis.from_url(settings.redis_url, decode_responses=True)
        self._prefix = f"agent_run:{agent_run_id}:"

    async def get(self, key: str) -> dict | list | None:
        raw = await self._redis.get(self._prefix + key)
        return json.loads(raw) if raw else None

    async def set(self, key: str, value: dict | list) -> None:
        await self._redis.set(self._prefix + key, json.dumps(value), ex=_TTL_SECONDS)

    async def close(self) -> None:
        await self._redis.aclose()
