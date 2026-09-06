"""pgvector-backed similarity search over ingested literature/label chunks."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def retrieve_literature_for_pair(rxcui_a: str, rxcui_b: str, db: AsyncSession | None = None) -> list[dict]:
    """Returns literature evidence items relevant to a candidate drug pair.

    NOTE: this is a structural stub. The production version should:
      1. embed a query like "interaction between {drug_a_name} and {drug_b_name}"
      2. run a pgvector cosine-similarity search against `literature_chunks`
      3. filter results below a relevance threshold
      4. return top-k as EvidenceItem-shaped dicts

    Wiring `db` through requires the retrieval_agent node to accept a session
    the same way patient_context_agent does — left as the natural next step
    once embeddings.py has a real provider configured.
    """
    logger.debug("Stub retrieval for pair (%s, %s) — no embeddings provider configured", rxcui_a, rxcui_b)
    return []
