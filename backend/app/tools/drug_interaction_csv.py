"""Local CSV-backed drug-drug interaction reference. Replaces the RxNorm
Interaction API (discontinued by NLM, Jan 2024) and OpenFDA label lookups
entirely as the ground-truth source for interaction_tool_agent.

Expected CSV columns: "Drug 1", "Drug 2", "Interaction Description".
"""
import csv
import functools
import logging
from pathlib import Path

from app.config import get_settings

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def _load_interactions() -> list[tuple[str, str, str]]:
    settings = get_settings()
    csv_path = Path(settings.drug_interactions_csv_path)

    if not csv_path.exists():
        logger.warning(
            "Drug interaction CSV not found at %s -- interaction checks will find nothing.",
            csv_path.resolve(),
        )
        return []

    rows: list[tuple[str, str, str]] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            drug1 = (row.get("Drug 1") or "").strip().lower()
            drug2 = (row.get("Drug 2") or "").strip().lower()
            description = (row.get("Interaction Description") or "").strip()
            if drug1 and drug2 and description:
                rows.append((drug1, drug2, description))

    logger.info("Loaded %s drug-drug interaction records from %s", len(rows), csv_path.resolve())
    return rows


def lookup_interaction(name_a: str, name_b: str) -> dict | None:
    """Bidirectional, case-insensitive substring match -- e.g. a CSV entry
    for "warfarin" matches a medication name of
    "warfarin sodium 5 mg oral tablet"."""
    a = (name_a or "").strip().lower()
    b = (name_b or "").strip().lower()
    if not a or not b:
        return None

    for drug1, drug2, description in _load_interactions():
        forward = drug1 in a and drug2 in b
        backward = drug1 in b and drug2 in a
        if forward or backward:
            return {"description": description}

    return None