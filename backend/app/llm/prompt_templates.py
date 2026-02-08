from typing import List
from langchain_core.documents import Document


SYSTEM_PROMPT = (
    "You are a secure internal company assistant.\n"
    "Answer ONLY using the provided context.\n"
    "Do NOT use any external or general knowledge.\n"
    "If the answer is not explicitly stated in the context, respond with:\n"
    "\"The requested information is not available in the provided documents.\""
)


def build_prompt(query: str, documents: List[Document]) -> str:
    context = "\n\n".join(
        f"[Source {i}]\n{doc.page_content}"
        for i, doc in enumerate(documents, 1)
    )

    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{query}\n\n"
        f"Answer:"
    )
