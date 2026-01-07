from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_db
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router

app = FastAPI(title="Hackathon Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hackathon Todo API is running"}
