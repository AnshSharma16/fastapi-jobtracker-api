
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

from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.job_schema import Job
from app.models.job import JobModel
from app.database.connection import SessionLocal

router = APIRouter()

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):

    jobs = db.query(JobModel).all()

    return jobs

@router.post("/jobs")
def create_job(job: Job,db:Session=Depends(get_db)):
    new_job=JobModel(
         company=job.company,
        role=job.role,
        status=job.status
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job added to database",
        "job": {
            "id": new_job.id,
            "company": new_job.company,
            "role": new_job.role,
            "status": new_job.status
        }
    }

