from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)  # Sin connect_args para MySQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency de sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
