from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.hired_employee import HiredEmployeeCreate, HiredEmployeeResponse
from crud.hired_employee import batch_insert_hired_employees

router = APIRouter(prefix="/hired_employees", tags=["Hired Employees"])

@router.post("/batch_insert", response_model=List[HiredEmployeeResponse])
def insert_hired_employees(employees: List[HiredEmployeeCreate], db: Session = Depends(get_db)):
    """
    Inserta de 1 a 2000 empleados contratados en una sola petición
    """
    if len(employees) == 0:
        raise HTTPException(status_code=400, detail="La lista está vacía")
    if len(employees) > 2000:
        raise HTTPException(status_code=400, detail="No puedes insertar más de 2000 registros por petición")

    inserted = batch_insert_hired_employees(db, employees)
    return inserted
