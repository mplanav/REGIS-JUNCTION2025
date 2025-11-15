# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router

# 👉 Importa Base y engine
from app.db.database import Base, engine
# 👉 Importa los modelos para que se registren en Base.metadata
from app.db import models  # noqa: F401  (se usa solo por side-effect)


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
    )

    # ------------------------------
    # CORS
    # ------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # en producción mejor restringir
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------
    # Rutas API
    # ------------------------------
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # ------------------------------
    # Crear tablas en startup
    # ------------------------------
    @app.on_event("startup")
    def startup_event():
        print("🔧 Creating DB tables if missing...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables ensured")

    return app


app = create_application()


@app.get("/")
def root():
    return {
        "message": "REGIS Backend MVP running",
        "api_prefix": settings.API_PREFIX
    }
