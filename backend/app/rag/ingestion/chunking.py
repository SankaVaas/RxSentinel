"""Splits literature/label text into overlapping chunks for embedding.

Simple fixed-window chunking; swap for a semantic/sentence-aware splitter
(e.g. LangChain's RecursiveCharacterTextSplitter) once ingestion volume
justifies it.
"""


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
