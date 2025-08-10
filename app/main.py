from fastapi import FastAPI
from core.database import Base, engine
from api.v1 import hired_employee
from api.v1 import departments
from api.v1 import jobs
# Crea tablas en la base de datos
#Base.metadata.create_all(bind=engine)

app = FastAPI(title="API - Hired Employees Batch Insert")

# Incluimos rutas

app.include_router(hired_employee.router)
app.include_router(departments.router)
app.include_router(jobs.router)