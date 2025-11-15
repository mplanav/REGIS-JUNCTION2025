# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# DATABASE_URL viene del docker-compose (backend.environment)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/regisdb")

# Conexión al motor de PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal: cada request usará una sesión de esto
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


# Dependency para usar en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
