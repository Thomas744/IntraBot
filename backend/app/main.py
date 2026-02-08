from fastapi import FastAPI
from backend.app.routes import auth_routes, chat_routes

app = FastAPI(
    title="Company Internal Chatbot Backend",
    version="1.0.0",
)

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)

@app.get("/")
def health():
    return {"status": "Backend is running"}



# "alice", "finance", "alice123"
# "bob", "marketing", "bob123"
# "carol", "hr", "carol123"
# "dave", "engineering", "dave123"
# "eve", "employees", "eve123"
# "admin", "c_level", "admin123"

# What is Year-Over-Year performance?
# employee salary
# financial report revenue