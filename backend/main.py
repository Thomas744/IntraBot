from fastapi import FastAPI
from backend.routes import auth_routes, chat_routes
from backend.routes.user_routes import router as user_router
from backend.rag.pipeline import run_pipeline_once

app = FastAPI(
    title="Company Internal Chatbot Backend",
    version="1.0.0",
)

@app.on_event("startup")
def startup_event():
    print("\n🔄 Building vector store (one-time)...")

    stats = run_pipeline_once()

    print("\n📊 DOCUMENT INGESTION SUMMARY")
    print("────────────────────────────────")

    for dept, count in sorted(stats["chunks_per_department"].items()):
        print(f"📁 {dept:<12} → {count} chunks")

    print("────────────────────────────────")
    print(f"✅ TOTAL DOCUMENT CHUNKS : {stats['total_chunks']}\n")

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(user_router) 

@app.get("/")
def health():
    return {"status": "Backend is running"}
