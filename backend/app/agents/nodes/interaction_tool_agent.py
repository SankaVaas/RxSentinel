"""Verifies each candidate pair against a local CSV of known drug-drug
interactions (app/tools/drug_interaction_csv.py). This is the node that
turns "the model thinks these interact" into "our reference dataset confirms
this interaction exists."
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.state import AgentState
from app.models.medication import Medication
from app.tools.drug_interaction_csv import lookup_interaction

logger = logging.getLogger(__name__)


async def run(state: AgentState, db: AsyncSession) -> dict:
    updated_candidates = []
    confirmed_count = 0

    for candidate in state["interaction_candidates"]:
        rxcui_a, rxcui_b = candidate["drug_pair"]

        med_a = await db.get(Medication, rxcui_a)
        med_b = await db.get(Medication, rxcui_b)
        name_a = med_a.name if med_a else rxcui_a
        name_b = med_b.name if med_b else rxcui_b

        evidence = list(candidate["evidence"])
        ground_truth_severity = None

        match = lookup_interaction(name_a, name_b)
        if match:
            # CSV has no severity field -- reasoning_agent assigns severity
            # from the description text; this flag just confirms a known
            # interaction exists in the reference dataset.
            ground_truth_severity = "moderate"
            evidence.append(
                {
                    "source": "csv_reference",
                    "citation": match["description"],
                    "url": None,
                    "excerpt": None,
                }
            )
            confirmed_count += 1

        updated_candidates.append(
            {
                **candidate,
                "ground_truth_severity": ground_truth_severity,
                "evidence": evidence,
            }
        )

    logger.info(
        "Checked %s pairs against CSV reference; %s matched",
        len(updated_candidates),
        confirmed_count,
    )
    return {"interaction_candidates": updated_candidates}