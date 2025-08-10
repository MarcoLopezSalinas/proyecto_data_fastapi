from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class HiredEmployeeBase(BaseModel):
    id: int
    name: Optional[str]
    datetime: Optional[datetime]
    department_id: Optional[int]
    job_id: Optional[int]

class HiredEmployeeCreate(HiredEmployeeBase):
    pass

class HiredEmployeeResponse(HiredEmployeeBase):
    class Config:
        orm_mode = True
