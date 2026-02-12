from typing import List, Tuple
from langchain_core.documents import Document

# Confidence based on similarity scores. Lower distance = higher relevance.
def calculate_confidence_from_scores(
    results: List[Tuple[Document, float]],
) -> float:
    

    if not results:
        return 0.0

    relevance_scores = [1 / (1 + score) for _, score in results]

    avg_score = sum(relevance_scores) / len(relevance_scores)

    return round(min(avg_score, 1.0), 2)
