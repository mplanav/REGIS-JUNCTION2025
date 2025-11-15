from fastapi import APIRouter

from .endpoints.risks import router as risks_router
from .endpoints.contradictions import router as contradictions_router
from .endpoints.overlaps import router as overlaps_router
from .endpoints.jurisdictions import router as jurisdictions_router
from .endpoints.documents import router as documents_router
from .endpoints.chat import router as chat_router

api_router = APIRouter()

api_router.include_router(risks_router, prefix="/risks", tags=["risks"])
api_router.include_router(contradictions_router, prefix="/contradictions", tags=["contradictions"])
api_router.include_router(overlaps_router, prefix="/overlaps", tags=["overlaps"])
api_router.include_router(jurisdictions_router, prefix="/jurisdictions", tags=["jurisdictions"])
api_router.include_router(documents_router, prefix="/documents", tags=["documents"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
