from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    role = Column(String)
    status = Column(String)