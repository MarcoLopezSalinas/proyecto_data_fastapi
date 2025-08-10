from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base  

class HiredEmployee(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    datetime = Column(DateTime, nullable=False)
    department_id = Column(Integer)
    job_id = Column(Integer)



