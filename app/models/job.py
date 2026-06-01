from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime,timezone
from app.database.connection import Base
import enum

class JobStatus(str, enum.Enum):
    applied = "Applied"
    screening = "Screening"
    interview = "Interview"
    offer = "Offer"
    rejected = "Rejected"
    withdrawn = "Withdrawn"

def utcnow():
    return datetime.now(timezone.utc)

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    role = Column(String)
    status = Column(String,nullable=False,default=JobStatus.applied)
    created_at = Column(DateTime(timezone=True),nullable=False,default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True),nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)
        