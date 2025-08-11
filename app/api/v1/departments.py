from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.departments import DepartmentResponse, DepartmentCreate
from crud.departments import batch_insert_departments

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/batch_insert", response_model=List[DepartmentResponse])
def insert_departments(departments: List[DepartmentCreate], db: Session = Depends(get_db)):
    """
    Inserta de 1 a 2000 departamentos en una sola petición
    """
    if len(departments) == 0:
        raise HTTPException(status_code=400, detail="La lista está vacía")
    if len(departments) > 2000:
        raise HTTPException(status_code=400, detail="No puedes insertar más de 2000 registros por petición")

    inserted = batch_insert_departments(db, departments)
    return inserted
