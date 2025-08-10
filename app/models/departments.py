from sqlalchemy import Column, Integer, String
from core.database import Base  
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String(100), nullable=False)