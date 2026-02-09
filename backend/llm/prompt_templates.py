from typing import List
from langchain_core.documents import Document

def build_prompt(query: str, documents: List[Document]) -> str:
    context = "\n\n".join(
        f"[Source {i}]\n{doc.page_content}"
        for i, doc in enumerate(documents, 1)
    )
    
    SYSTEM_PROMPT = (
        "You are an internal company Q&A assistant. \n"
        "Instructions: \n"
        "- Answer using ONLY the information in the context. \n"
        "- Extract factual points relevant to the question. \n"
        "- Do NOT add new information. \n"
        "- Present the answer clearly in 3–5 bullet points. \n"
        "- If the answer is not present, reply exactly: I don't know. \n"
        "Context: {context} \n"
        "Question: {query} \n"
        "Answer: \n" 
    )

    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Context:\n{context}\n\n"
        f"User Query:\n{query}\n\n"
        f"Answer:"
    )
