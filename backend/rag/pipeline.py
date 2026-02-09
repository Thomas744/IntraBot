from backend.rag.preprocessing import preprocess
from backend.rag.vector_store import build_vector_store
from pathlib import Path

BASE_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "Fintech-data"


def run_pipeline_once():
    directories = [d for d in BASE_DATA_PATH.iterdir() if d.is_dir()]
    result = preprocess(directories)
    build_vector_store(result["documents"])

    return {
        "total_documents": result["total_documents"],
        "total_chunks": result["total_chunks"],
    }
