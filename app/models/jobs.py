from sqlalchemy import Column, Integer, String
from core.database import Base  
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String(100), nullable=False)