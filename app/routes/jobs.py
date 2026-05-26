
'''from fastapi import APIRouter
router=APIRouter()

@router.get('/jobs')
def get_jobs():
    return [
    {
        "company": "OpenAI",
            "role": "Python Backend Intern"
    },
    {
         "company": "Anthropic",
            "role": "AI Automation Developer"
    }
    ]'''

from fastapi import APIRouter
from app.schemas.job_schema import Job

router = APIRouter()

jobs_db = []

@router.get("/jobs")
def get_jobs():
    return jobs_db

@router.post("/jobs")
def create_job(job: Job):
    jobs_db.append(job.dict())
    return {
        "message": "Job added successfully",
        "job": job
    }