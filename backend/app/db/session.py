from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@postgres:5432/regis"
    )

    class Config:
        env_file = ".env"

settings = Settings()

# SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
)

# SessionLocal: used for each backend request
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for ORM models
Base = declarative_base()

# FastAPI dependency: yields a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
