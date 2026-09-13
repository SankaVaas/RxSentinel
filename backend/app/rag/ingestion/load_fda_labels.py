"""Bulk ingestion script for OpenFDA drug label `drug_interactions` sections
into the pgvector literature store, for RAG retrieval at agent runtime
(separate from the live per-request OpenFDA lookups in tools/openfda_client.py,
which fetch fresh data for the *specific* candidate pair being checked).

Usage:
    python -m app.rag.ingestion.load_fda_labels --limit 5000
"""
import argparse
import asyncio
import logging

from app.tools.base_tool import get_json
from app.config import get_settings

logger = logging.getLogger(__name__)


async def main(limit: int) -> None:
    settings = get_settings()
    url = f"{settings.openfda_api_base}/drug/label.json"
    params = {"search": "_exists_:drug_interactions", "limit": min(limit, 100)}

    data = await get_json(url, params=params)
    results = data.get("results", [])
    logger.info("Fetched %s labels with drug_interactions sections", len(results))

    # TODO: chunk each result's drug_interactions text, embed, upsert to pgvector.
    raise NotImplementedError("Wire up chunking + embeddings.embed_text + DB upsert")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()
    asyncio.run(main(args.limit))
