"""Client for OpenFDA drug label data — used to pull boxed warnings and
drug-interaction sections directly from FDA-approved labeling as
corroborating evidence alongside the curated interaction reference.

Docs: https://open.fda.gov/apis/drug/label/
"""
import logging

import httpx

from app.config import get_settings
from app.tools.base_tool import get_json

logger = logging.getLogger(__name__)


async def fetch_label_warnings(rxcui_a: str, rxcui_b: str) -> list[dict]:
    """Returns a list of evidence items sourced from FDA label
    `drug_interactions` sections, if either drug's label mentions the other.

    A 404 here just means OpenFDA has no label indexed for that RxCUI --
    common for generics or drugs indexed under a different RxCUI -- so it's
    treated as "no evidence found," not an error.
    """
    settings = get_settings()
    evidence: list[dict] = []

    for rxcui in (rxcui_a, rxcui_b):
        url = f"{settings.openfda_api_base}/drug/label.json"
        params = {"search": f"openfda.rxcui:{rxcui}", "limit": 1}
        try:
            data = await get_json(url, params=params)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                continue  # no label indexed for this rxcui -- not an error
            logger.warning("OpenFDA label lookup returned %s for rxcui=%s", exc.response.status_code, rxcui)
            continue
        except Exception:  # noqa: BLE001
            logger.exception("OpenFDA label lookup failed for rxcui=%s", rxcui)
            continue

        results = data.get("results", [])
        if not results:
            continue

        label = results[0]
        interaction_text = label.get("drug_interactions", [])
        if interaction_text:
            evidence.append(
                {
                    "source": "openfda",
                    "citation": f"FDA label, drug_interactions section (rxcui={rxcui})",
                    "url": f"https://labels.fda.gov/?rxcui={rxcui}",
                    "excerpt": interaction_text[0][:500],
                }
            )

    return evidence