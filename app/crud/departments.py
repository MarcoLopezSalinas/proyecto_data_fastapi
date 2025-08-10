from sqlalchemy.orm import Session
from models.departments import Department
from schemas.departments import DepartmentCreate

def batch_insert_departments(db: Session, departments: list[DepartmentCreate]):
    """
    Inserta de 1 a 1000 departamentos en una sola operación
    """
    department_objects = []
    for department in departments:
        dept = Department(
            id=department.id,
            department=department.department
        )
        department_objects.append(dept)

    db.bulk_save_objects(department_objects)
    db.commit()
    return department_objects
