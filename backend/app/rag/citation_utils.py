from typing import List, Dict
from langchain_core.documents import Document


def extract_citations(documents: List[Document]) -> List[Dict]:
    """
    Extracts unique source citations from retrieved documents.
    """
    seen = set()
    citations = []

    for idx, doc in enumerate(documents, 1):
        source = doc.metadata.get("source_path")
        department = doc.metadata.get("department")

        key = (source, department)
        if key in seen:
            continue

        seen.add(key)
        citations.append({
            "id": idx,
            "source_path": source,
            "department": department,
        })

    return citations
