# app/api/v1/risks.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.ai.risk_description import RISK_DESCRIPTIONS
from app.ai.risk_mock_data import MOCK_PERCENTAGES

from app.db.database import get_db
from app.db.models import Requirement, RiskTypeEnum

router = APIRouter()


# -----------------------------------------------------------
# GET /risks/types
# -----------------------------------------------------------
@router.get("/types")
def get_risk_types():
    """
    Devuelve la lista de tipos de riesgo.
    """
    return [rt.value for rt in RiskTypeEnum]


# -----------------------------------------------------------
# GET /risks
# -----------------------------------------------------------
@router.get("/")
def list_risks(
    db: Session = Depends(get_db),
    risk_type: str | None = Query(None),
    jurisdiction: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    Lista requerimientos filtrando por:
    - risk_type
    - jurisdiction
    Con soporte de paginación.
    """

    query = db.query(Requirement)

    if risk_type:
        query = query.filter(Requirement.risk_type == risk_type)

    if jurisdiction:
        query = query.filter(Requirement.jurisdiction == jurisdiction)

    results = query.offset(offset).limit(limit).all()
    return results


# -----------------------------------------------------------
# GET /risks/{id}
# -----------------------------------------------------------
@router.get("/{req_id}")
def get_risk(req_id: int, db: Session = Depends(get_db)):
    """
    Devuelve un requirement por su ID.
    """
    req = db.query(Requirement).filter(Requirement.id == req_id).first()

    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")

    return req


@router.get("/risks/percentages")
def get_risk_percentages():
    # Mock ahora – luego se cambia por DB o por embeddings/classifier real
    return MOCK_PERCENTAGES


@router.get("/risks/{category}")
def get_risk_details(category: str):
    category = category.upper()
    if category not in RISK_DESCRIPTIONS:
        raise HTTPException(status_code=404, detail="Unknown risk category")

    return {
        "category": category,
        "description": RISK_DESCRIPTIONS[category]
    }