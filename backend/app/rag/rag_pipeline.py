from backend.app.rag.pipeline import run_pipeline
from backend.app.rag.retriever import secure_search_with_scores
from backend.app.rag.citation_utils import extract_citations
from backend.app.rag.confidence_utils import calculate_confidence_from_scores
from backend.app.llm.llm_client import LLMClient
from backend.app.llm.prompt_templates import build_prompt


FALLBACK_MESSAGE = "The requested information is not available in the provided documents."


class RAGPipeline:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, user_role: str, query: str, k: int = 5):
        pipeline_result = run_pipeline(user_role)
        store = pipeline_result["vector_store"]

        results = secure_search_with_scores(store, query, user_role, k)

        if not results:
            return {
                "answer": FALLBACK_MESSAGE,
                "confidence": 0.0,
                "citations": [],
            }

        documents = [doc for doc, _ in results]

        prompt = build_prompt(query, documents)
        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "confidence": calculate_confidence_from_scores(results),
            "citations": extract_citations(documents),
        }
