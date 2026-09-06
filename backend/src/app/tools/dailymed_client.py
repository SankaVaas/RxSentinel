"""Client for DailyMed SPL (Structured Product Labeling) data. Used as a
secondary label source when OpenFDA lacks a current label for a given RxCUI.

Docs: https://dailymed.nlm.nih.gov/dailymed/app-support-web-services.cfm
"""
import logging

from app.config import get_settings
from app.tools.base_tool import get_json

logger = logging.getLogger(__name__)


async def fetch_spl_by_rxcui(rxcui: str) -> dict | None:
    settings = get_settings()
    url = f"{settings.dailymed_api_base}/spls.json"
    params = {"rxcui": rxcui}

    try:
        data = await get_json(url, params=params)
    except Exception: 
        logger.exception("DailyMed lookup failed for rxcui=%s", rxcui)
        return None

    entries = data.get("data", [])
    return entries[0] if entries else None
