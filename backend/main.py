from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv

from backend.routes import auth_routes, chat_routes
from backend.routes.user_routes import router as user_router
from backend.rag.pipeline import run_pipeline_once
from backend.rag.vector_store import PERSIST_DIR

from backend.db.database import SessionLocal
from backend.db.models import UserDB
from backend.auth.password_utils import hash_password

load_dotenv()

app = FastAPI(
    title="Company Internal Chatbot Backend",
    version="1.0.0",
)


FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL] if FRONTEND_URL != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ensure_default_admin():
    db = SessionLocal()
    try:
        username = os.getenv("DEFAULT_ADMIN_USERNAME")
        password = os.getenv("DEFAULT_ADMIN_PASSWORD")
        role = os.getenv("DEFAULT_ADMIN_ROLE")

        if not username or not password:
            print("⚠️ DEFAULT_ADMIN_USERNAME or DEFAULT_ADMIN_PASSWORD not set")
            return

        admin_user = (
            db.query(UserDB)
            .filter(UserDB.username == username)
            .first()
        )

        if not admin_user:
            print("Creating default admin user...")
            new_admin = UserDB(
                username=username,
                role=role,
                hashed_password=hash_password(password),
            )
            db.add(new_admin)
            db.commit()
            print("Default admin created.")
        else:
            print("Admin already exists.")

    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    print("Backend starting...")

    ensure_default_admin()

    persist_path = Path(PERSIST_DIR)

    if not persist_path.exists():
        print("Vector store not found. Building...")

        stats = run_pipeline_once()

        print("Document Ingestion Summary")
        for dept, count in sorted(stats["chunks_per_department"].items()):
            print(f"{dept} → {count} chunks")

        print(f"TOTAL CHUNKS: {stats['total_chunks']}")
    else:
        print("Existing vector store detected. Skipping rebuild.")

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(user_router)

@app.get("/")
def health():
    return {"status": "Backend is running"}
