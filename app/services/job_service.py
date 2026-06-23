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
    current_user,
    db: Session,
    status: Optional[JobStatus] = None,
    skip:int=0,
    limit:int=10
):
    query = db.query(
    JobModel
).filter(
    JobModel.user_id == current_user.id
)
    if status:
        query = query.filter(
            JobModel.status == status
        )
    return query.order_by(
        JobModel.created_at.desc()
    ).offset(skip)\
    .limit(limit)\
    .all()

def count_jobs(db: Session):
    return db.query(
        JobModel
    ).count()

def get_job_by_id(job_id: int, current_user, db: Session):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()

    if job.user_id != current_user.id:
        raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

def create_job(job_data: JobCreate,current_user, db: Session):

    new_job = JobModel(
        company=job_data.company,
        role=job_data.role,
        status=job_data.status,
        salary=job_data.salary,
        user_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


def update_job(
    job_id: int,
    job_data: JobUpdate,
    current_user,
    db: Session
):
    job = get_job_by_id(job_id, db)

    if job.user_id != current_user.id:
        raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )

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
    current_user,
    db: Session
):
    job = get_job_by_id(job_id, db)

    if job.user_id != current_user.id:
        raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }

