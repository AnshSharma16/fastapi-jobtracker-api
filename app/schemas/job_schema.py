from pydantic import BaseModel,ConfigDict,field_validator
from app.models.job import JobStatus
from datetime import datetime
from typing import Optional

class JobCreate(BaseModel):
    company: str
    role: str
    status: JobStatus = JobStatus.applied
    salary: int | None = None

    @field_validator("company", "role")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty or whitespace")
        return v.strip()
    
class JobUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[JobStatus] = None
    salary: Optional[int] = None

    @field_validator("company", "role")
    @classmethod
    def must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Field cannot be empty or whitespace")
        return v.strip() if v else v
    
class JobResponse(BaseModel):
    id:int
    company: str
    role: str
    status: str
    salary: int | None = None
    user_id: int | None = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)