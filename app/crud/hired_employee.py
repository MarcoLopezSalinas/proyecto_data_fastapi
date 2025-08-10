from sqlalchemy.orm import Session
from models.hired_employee import HiredEmployee
from schemas.hired_employee import HiredEmployeeCreate
HiredEmployeeCreate
def batch_insert_hired_employees(db: Session, employees: list[HiredEmployeeCreate]):
    """
    Inserta de 1 a 1000 empleados en una sola operación
    """
    hired_employee_objects = []
    for employee in employees:
        hired_employee = HiredEmployee(
            id=employee.id,
            name=employee.name,
            datetime=employee.datetime,
            department_id=employee.department_id,
            job_id=employee.job_id
        )
        hired_employee_objects.append(hired_employee)

    db.bulk_save_objects(hired_employee_objects)
    db.commit()
    return hired_employee_objects
