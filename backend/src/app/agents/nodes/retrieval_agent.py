"""RAG node: retrieves relevant literature/label excerpts for the patient's
active medication list from the pgvector-backed store. This surfaces
*candidate* interaction pairs and mechanistic context — it is deliberately
not treated as ground truth; interaction_tool_agent verifies against
structured data before anything is surfaced to a clinician.
"""
import logging
from itertools import combinations

from app.agents.state import AgentState, InteractionCandidate
from app.rag.retriever import retrieve_literature_for_pair

logger = logging.getLogger(__name__)


async def run(state: AgentState) -> dict:
    rxcuis = state["patient_context"]["active_rxcuis"]
    candidates: list[InteractionCandidate] = []

    for rxcui_a, rxcui_b in combinations(sorted(rxcuis), 2):
        evidence = await retrieve_literature_for_pair(rxcui_a, rxcui_b)
        candidates.append(
            {
                "drug_pair": (rxcui_a, rxcui_b),
                "ground_truth_severity": None,
                "llm_flagged": len(evidence) > 0,
                "evidence": evidence,
            }
        )

    logger.info("Retrieved literature context for %s drug pairs", len(candidates))
    return {"interaction_candidates": candidates}
