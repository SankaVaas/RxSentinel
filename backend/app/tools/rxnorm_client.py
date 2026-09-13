"""Client for the NIH RxNorm API -- used only for drug-name search/typeahead
now. Interaction verification is handled entirely by
app/tools/drug_interaction_csv.py.
"""
import logging

from app.config import get_settings
from app.tools.base_tool import get_json

logger = logging.getLogger(__name__)


async def approximate_search(term: str, max_results: int = 8) -> list[dict]:
    settings = get_settings()
    url = f"{settings.rxnorm_api_base}/approximateTerm.json"
    params = {"term": term, "maxEntries": max_results}

    try:
        data = await get_json(url, params=params)
    except Exception:  # noqa: BLE001
        logger.exception("RxNorm approximate search failed for term=%s", term)
        return []

    candidates = data.get("approximateGroup", {}).get("candidate", [])
    results = []
    seen_rxcuis: set[str] = set()

    for candidate in candidates:
        rxcui = candidate.get("rxcui")
        if not rxcui or rxcui in seen_rxcuis:
            continue
        seen_rxcuis.add(rxcui)
        name = await _get_name_for_rxcui(rxcui)
        if name:
            results.append({"rxcui": rxcui, "name": name})

    return results


async def _get_name_for_rxcui(rxcui: str) -> str | None:
    settings = get_settings()
    url = f"{settings.rxnorm_api_base}/rxcui/{rxcui}/property.json"
    params = {"propName": "RxNorm Name"}
    try:
        data = await get_json(url, params=params)
    except Exception:  # noqa: BLE001
        return None
    props = data.get("propConceptGroup", {}).get("propConcept", [])
    return props[0]["propValue"] if props else None