"""Shared HTTP client wrapper: retry, timeout, and structured logging for
every external clinical-data API call. Centralizing this is what makes the
audit trail trustworthy — every tool call an agent makes is logged the same
way, regardless of which external API it hits.
"""
import logging

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
async def get_json(url: str, params: dict | None = None) -> dict | list:
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        logger.debug("GET %s params=%s", url, params)
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
