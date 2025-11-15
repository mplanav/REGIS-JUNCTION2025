# app/api/v1/contradictions.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Contradiction

router = APIRouter()


# -----------------------------------------------------------
# GET /contradictions
# -----------------------------------------------------------
@router.get("/")
def list_contradictions(
    db: Session = Depends(get_db),
    jurisdiction: str | None = Query(None),
    requirement_id: int | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    Lista contradicciones, con filtros opcionales:
    - jurisdiction
    - requirement_id (si quieres ver contradicciones relacionadas con 1 req)
    """

    query = db.query(Contradiction)

    if jurisdiction:
        query = query.filter(Contradiction.jurisdiction == jurisdiction)

    if requirement_id:
        query = query.filter(
            (Contradiction.requirement1_id == requirement_id) |
            (Contradiction.requirement2_id == requirement_id)
        )

    results = query.offset(offset).limit(limit).all()
    return results


# -----------------------------------------------------------
# GET /contradictions/{id}
# -----------------------------------------------------------
@router.get("/{contradiction_id}")
def get_contradiction(
    contradiction_id: int,
    db: Session = Depends(get_db)
):
    """
    Devuelve una contradicción por ID.
    """

    c = (
        db.query(Contradiction)
        .filter(Contradiction.id == contradiction_id)
        .first()
    )

    if not c:
        raise HTTPException(status_code=404, detail="Contradiction not found")

    return c
