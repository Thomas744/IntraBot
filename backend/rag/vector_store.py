from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path
import shutil
import os

DATA_DIR = Path(os.getenv("DATA_DIR", "backend/vector_db"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

PERSIST_DIR = str(DATA_DIR / "chroma")
_COLLECTION_NAME = "company_docs"

_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
_vector_store: Chroma | None = None


def build_vector_store(documents: List[Document]) -> Chroma:
    global _vector_store

    persist_path = Path(PERSIST_DIR)
    if persist_path.exists():
        shutil.rmtree(persist_path)

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

    persist_path = Path(PERSIST_DIR)
    if not persist_path.exists():
        raise RuntimeError("Vector store not found.")

    _vector_store = Chroma(
        embedding_function=_embeddings,
        persist_directory=PERSIST_DIR,
        collection_name=_COLLECTION_NAME,
    )

    return _vector_store
