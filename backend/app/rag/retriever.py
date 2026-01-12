from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma


def secure_search(
    vector_store: Chroma,
    query: str,
    role: str,
    k: int = 5,
) -> List[Document]:

    results = vector_store.similarity_search(query, k=k * 2)
    safe = []

    for doc in results:
        roles = doc.metadata.get("accessible_roles", "")
        if role in roles:
            safe.append(doc)
        if len(safe) == k:
            break

    return safe
