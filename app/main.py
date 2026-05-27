from fastapi import FastAPI
from app.routes.jobs import router as jobs_router
from app.database.connection import engine
from app.models.job import JobModel

Base = JobModel.metadata
Base.create_all(bind=engine)


app = FastAPI(
    title="Job Tracker API",
    version="1.0.0"
)

app.include_router(jobs_router)

@app.get("/")
def home():
    return {
        "message": "FastAPI Job Tracker API Running"
    }