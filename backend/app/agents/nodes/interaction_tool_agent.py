"""Verifies each candidate pair against structured, authoritative sources
(RxNorm interaction API, OpenFDA label data) rather than relying on the LLM's
parametric knowledge. This is the node that turns "the model thinks these
interact" into "NIH's interaction dataset confirms these interact, severity=X".
"""
import logging

from app.agents.state import AgentState
from app.tools.rxnorm_client import check_interaction
from app.tools.openfda_client import fetch_label_warnings

logger = logging.getLogger(__name__)


async def run(state: AgentState) -> dict:
    updated_candidates = []

    for candidate in state["interaction_candidates"]:
        rxcui_a, rxcui_b = candidate["drug_pair"]
        ground_truth = await check_interaction(rxcui_a, rxcui_b)

        evidence = list(candidate["evidence"])
        if ground_truth:
            evidence.append(
                {
                    "source": "rxnorm",
                    "citation": ground_truth["description"],
                    "url": ground_truth.get("source_url"),
                    "excerpt": None,
                }
            )
            label_warnings = await fetch_label_warnings(rxcui_a, rxcui_b)
            evidence.extend(label_warnings)

        updated_candidates.append(
            {
                **candidate,
                "ground_truth_severity": ground_truth["severity"] if ground_truth else None,
                "evidence": evidence,
            }
        )

    logger.info(
        "Verified %s pairs; %s confirmed by structured ground truth",
        len(updated_candidates),
        sum(1 for c in updated_candidates if c["ground_truth_severity"]),
    )
    # Replace rather than append: this node enriches the same candidates.
    return {"interaction_candidates": updated_candidates}
