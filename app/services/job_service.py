from fastapi import HTTPException
from typing import Optional
from app.models.job import JobStatus
from sqlalchemy.orm import Session
from app.models.job import JobModel
from app.schemas.job_schema import (
    JobCreate,
    JobUpdate
)

def get_all_jobs(
    db: Session,
    status: Optional[JobStatus] = None
):
    query = db.query(JobModel)
    if status:
        query = query.filter(
            JobModel.status == status
        )
    return query.all()

def get_job_by_id(job_id: int, db: Session):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

def create_job(job_data: JobCreate, db: Session):

    new_job = JobModel(
        company=job_data.company,
        role=job_data.role,
        status=job_data.status
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session
):
    job = get_job_by_id(job_id, db)

    update_data = job_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


def delete_job(
    job_id: int,
    db: Session
):
    job = get_job_by_id(job_id, db)

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }