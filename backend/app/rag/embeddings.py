"""Embedding generation for the RAG literature/label store.

Uses Anthropic-compatible embedding provider (Voyage AI is Anthropic's
recommended embeddings partner). Kept as a thin wrapper so the provider can
be swapped without touching retriever.py.
"""
from app.config import get_settings


async def embed_text(text: str) -> list[float]:
    """Returns a dense embedding vector for the given text.

    Placeholder implementation: wire up `voyageai` or another embeddings
    client here. Kept as an explicit stub rather than a fake vector so it
    fails loudly if called before configured, instead of silently returning
    garbage embeddings.
    """
    raise NotImplementedError(
        "Wire up an embeddings provider (e.g. voyageai.Client().embed) before "
        "running ingestion or retrieval."
    )
