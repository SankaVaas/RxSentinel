"""Ingestion script for DrugBank interaction data (requires a DrugBank
academic/commercial license — data is not redistributed with this repo).

Usage:
    python -m app.rag.ingestion.load_drugbank --input path/to/drugbank.xml
"""
import argparse
import logging

logger = logging.getLogger(__name__)


def main(input_path: str) -> None:
    raise NotImplementedError(
        "Parse DrugBank XML export, extract drug-interaction descriptions, "
        "chunk via chunking.chunk_text, embed via embeddings.embed_text, "
        "and upsert into the pgvector `literature_chunks` table."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    main(args.input)
