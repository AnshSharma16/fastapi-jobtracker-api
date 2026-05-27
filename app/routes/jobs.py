
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

@router.put("/jobs/{job_id}")
def update_job(
    job_id: int,
    updated_job: Job,
    db: Session = Depends(get_db)
):

    job = db.query(JobModel).filter(JobModel.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    job.company = updated_job.company
    job.role = updated_job.role
    job.status = updated_job.status

    db.commit()
    db.refresh(job)

    return {
        "message": "Job updated successfully",
        "job": job
    }

@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):

    job = db.query(JobModel).filter(JobModel.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }