from fastapi import FastAPI
from app.routes.jobs import router as jobs_router
from app.database.connection import Base, engine
from app.routes.users import router as users_router

app = FastAPI(
    title="Job Tracker API",
    version="1.0.0"
)

app.include_router(jobs_router)
app.include_router(users_router)

@app.get("/")
def home():
    return {
        "message": "FastAPI Job Tracker API Running"
    }