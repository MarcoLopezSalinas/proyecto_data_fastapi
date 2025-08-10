from sqlalchemy.orm import Session
from models.jobs import Job
from schemas.jobs import JobCreate
def batch_insert_jobs(db: Session, jobs: list[JobCreate]):
    """
    Inserta de 1 a 1000 trabajos en una sola operación
    """
    job_objects = []
    for job in jobs:
        job_obj = Job(
            id=job.id,
            job=job.job
        )
        job_objects.append(job_obj)

    db.bulk_save_objects(job_objects)
    db.commit()
    return job_objects