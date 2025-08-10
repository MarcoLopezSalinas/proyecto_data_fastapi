from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.jobs import JobResponse, JobCreate
from crud.jobs import batch_insert_jobs

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/batch_insert", response_model=List[JobResponse])
def insert_jobs(jobs: List[JobCreate], db: Session = Depends(get_db)):
    """
    Inserta de 1 a 1000 trabajos en una sola petición
    """
    if len(jobs) == 0:
        raise HTTPException(status_code=400, detail="La lista está vacía")
    if len(jobs) > 1000:
        raise HTTPException(status_code=400, detail="No puedes insertar más de 1000 registros por petición")

    inserted = batch_insert_jobs(db, jobs)
    return inserted