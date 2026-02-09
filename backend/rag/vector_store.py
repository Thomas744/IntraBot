from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path

PERSIST_DIR = "backend/vector_db/chroma"
_COLLECTION_NAME = "company_docs"

_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
_vector_store: Chroma | None = None


def build_vector_store(documents: List[Document]) -> Chroma:
    global _vector_store

    _vector_store = Chroma.from_documents(
        documents=documents,
        embedding=_embeddings,
        persist_directory=PERSIST_DIR,
        collection_name=_COLLECTION_NAME,
    )
    return _vector_store


def get_vector_store() -> Chroma:
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    if Path(PERSIST_DIR).exists():
        _vector_store = Chroma(
            embedding_function=_embeddings,
            persist_directory=PERSIST_DIR,
            collection_name=_COLLECTION_NAME,
        )
        return _vector_store

    raise RuntimeError(
        "Vector store not ready yet. Startup event has not run."
    )
