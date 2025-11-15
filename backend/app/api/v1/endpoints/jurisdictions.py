# app/api/v1/jurisdictions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Requirement, JurisdictionEnum

router = APIRouter()


# -----------------------------------------------------------
# GET /jurisdictions
# -----------------------------------------------------------
@router.get("/")
def list_jurisdictions():
    """
    Devuelve todas las jurisdicciones disponibles.
    """
    return [j.value for j in JurisdictionEnum]


# -----------------------------------------------------------
# GET /jurisdictions/{jurisdiction}/requirements
# -----------------------------------------------------------
@router.get("/{jurisdiction}/requirements")
def list_requirements_by_jurisdiction(
    jurisdiction: str,
    db: Session = Depends(get_db)
):
    """
    Devuelve todos los requirements de una jurisdicción concreta.
    """

    # Validamos que existe ese jurisdiction
    JURIS = [j.value for j in JurisdictionEnum]

    if jurisdiction not in JURIS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid jurisdiction. Must be one of: {JURIS}"
        )

    reqs = (
        db.query(Requirement)
        .filter(Requirement.jurisdiction == jurisdiction)
        .all()
    )

    return reqs
