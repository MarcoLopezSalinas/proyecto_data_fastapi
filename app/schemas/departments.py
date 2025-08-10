from pydantic import BaseModel

class DepartmentBase(BaseModel):
    id: int
    department: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    pass
    class Config:
        orm_mode = True