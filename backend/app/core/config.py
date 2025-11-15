# app/core/config.py

import os
from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "REGIS Backend MVP"
    API_PREFIX: str = "/api/v1"

    # La variable real viene del entorno
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/regisdb"
    )

    # Reservado para futuro: la API key de OpenAI, etc.
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

    class Config:
        arbitrary_types_allowed = True


settings = Settings()
