# app/api/v1/overlaps.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Overlap

router = APIRouter()


# -----------------------------------------------------------
# GET /overlaps
# -----------------------------------------------------------
@router.get("/")
def list_overlaps(
    db: Session = Depends(get_db),
    jurisdiction: str | None = Query(None),
    requirement_id: int | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    Lista overlaps con filtros opcionales:
    - jurisdiction
    - requirement_id (para ver overlaps relacionados con un requirement)
    """

    query = db.query(Overlap)

    if jurisdiction:
        query = query.filter(Overlap.jurisdiction == jurisdiction)

    if requirement_id:
        query = query.filter(
            (Overlap.requirement1_id == requirement_id) |
            (Overlap.requirement2_id == requirement_id)
        )

    results = query.offset(offset).limit(limit).all()
    return results


# -----------------------------------------------------------
# GET /overlaps/{id}
# -----------------------------------------------------------
@router.get("/{overlap_id}")
def get_overlap(
    overlap_id: int,
    db: Session = Depends(get_db)
):
    """
    Devuelve un overlap por ID.
    """

    ov = (
        db.query(Overlap)
        .filter(Overlap.id == overlap_id)
        .first()
    )

    if not ov:
        raise HTTPException(status_code=404, detail="Overlap not found")

    return ov
