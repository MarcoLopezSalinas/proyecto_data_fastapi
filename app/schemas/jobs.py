from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class JobBase(BaseModel):
    id: int
    job: Optional[str]

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    class Config:
        orm_mode = True