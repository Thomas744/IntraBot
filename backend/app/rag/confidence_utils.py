from typing import List, Tuple
from langchain_core.documents import Document


def calculate_confidence_from_scores(
    results: List[Tuple[Document, float]],
) -> float:
    """
    Confidence based on similarity scores.
    Lower distance = higher relevance.
    """

    if not results:
        return 0.0

    # Convert distances to relevance scores
    relevance_scores = [1 / (1 + score) for _, score in results]

    avg_score = sum(relevance_scores) / len(relevance_scores)

    return round(min(avg_score, 1.0), 2)
