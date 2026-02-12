from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.auth.dependencies import get_current_user
from backend.auth.audit_logger import log_access
from backend.rag.rag_pipeline import rag_pipeline

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def query_docs(
    request: QueryRequest,
    user=Depends(get_current_user),
):
    result = rag_pipeline.run(
        user_role=user.role,
        query=request.query,
        k=5,
    )

    log_access(
        username=user.username,
        role=user.role,
        query=request.query,
        results_count=len(result["citations"]),
    )

    return {
        "user": user.username,
        "role": user.role,
        "query": request.query,
        "answer": result["answer"],
        "confidence": result["confidence"],
        "citations": result["citations"],
    }
