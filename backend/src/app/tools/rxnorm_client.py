"""Client for the NIH RxNorm / RxNav interaction API — the primary
structured ground-truth source for drug-drug interaction checks.

Docs: https://lhncbc.nlm.nih.gov/RxNav/APIs/InteractionAPIs.html
"""
import logging

from app.config import get_settings
from app.tools.base_tool import get_json

logger = logging.getLogger(__name__)

_SEVERITY_MAP = {
    "N/A": None,
    "minor": "low",
    "moderate": "moderate",
    "major": "high",
    "contraindicated": "contraindicated",
}


async def check_interaction(rxcui_a: str, rxcui_b: str) -> dict | None:
    """Returns {"severity": ..., "description": ..., "source_url": ...} or
    None if no interaction is found between the two RxCUIs."""
    settings = get_settings()
    url = f"{settings.rxnorm_api_base}/interaction/list.json"
    params = {"rxcuis": f"{rxcui_a}+{rxcui_b}"}

    try:
        data = await get_json(url, params=params)
    except Exception: 
        logger.exception("RxNorm interaction lookup failed for %s/%s", rxcui_a, rxcui_b)
        return None

    groups = data.get("fullInteractionTypeGroup", [])
    if not groups:
        return None

    # Flatten first reported interaction pair — a production version should
    # aggregate across all interaction types/sources returned, not just [0].
    first_type = groups[0]["fullInteractionType"][0]
    interaction_pair = first_type["interactionPair"][0]

    raw_severity = interaction_pair.get("severity", "N/A")
    return {
        "severity": _SEVERITY_MAP.get(raw_severity, "moderate"),
        "description": interaction_pair.get("description", ""),
        "source_url": "https://rxnav.nlm.nih.gov/",
    }
