from fastapi import APIRouter, Depends, status
from app.core.security import get_current_user
from app.models.user import UserModel
from sqlalchemy.orm import Session
from typing import Optional
from app.models.job import JobStatus
from app.database.connection import get_db
from app.schemas.job_schema import (
    JobCreate,
    JobUpdate,
    JobResponse
)
from app.services import job_service

router = APIRouter()


@router.get(
    "/jobs",
    response_model=list[JobResponse]
)
def get_jobs(
    status: Optional[JobStatus] = None,
    skip: int = 0,
    limit: int = 10,
    current_user: UserModel = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):
    return job_service.get_all_jobs(
        current_user,
        db,
        status,
        skip,
        limit
    )

@router.get("/jobs/count")
def count_jobs(
    db: Session = Depends(get_db)
):
    return {
        "count":
        job_service.count_jobs(db)
    }

@router.get(
    "/jobs/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    return job_service.get_job_by_id(
        job_id,
        db
    )

@router.post(
    "/jobs",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_job(
    job: JobCreate,
    current_user: UserModel = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return job_service.create_job(
        job,
        current_user,
        db
    )

@router.patch(
    "/jobs/{job_id}",
    response_model=JobResponse
)
def update_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db)
):
    return job_service.update_job(
        job_id,
        job,
        db
    )


@router.delete(
    "/jobs/{job_id}"
)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    return job_service.delete_job(
        job_id,
        db
    )


