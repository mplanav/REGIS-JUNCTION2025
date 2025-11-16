from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import random

from app.db.database import get_db
from app.db.models.requirements import Requirement


router = APIRouter(prefix="/requirements", tags=["Requirements"])


# ------------------------------------------------------------
#  Helper data (simulated descriptions)
# ------------------------------------------------------------

SUGGESTED_SENTENCES = [
    "This regulation provides baseline compliance requirements.",
    "A standard obligation that applies across general business operations.",
    "Commonly referenced rule providing essential legal guidance.",
    "General compliance requirement applicable in most jurisdictions.",
    "A typical regulation that ensures baseline regulatory alignment."
]


# ------------------------------------------------------------
# GET /api/v1/requirements/list
# Returns all normal requirements (not interactions)
# ------------------------------------------------------------
@router.get("/list")
def list_requirements(
    jurisdiction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Returns the list of 'normal' requirements.
    These are not contradictions or overlaps — just standalone rules.
    """

    query = db.query(Requirement)

    if jurisdiction:
        query = query.filter(Requirement.jurisdiction == jurisdiction)

    requirements = query.all()

    results = []
    for req in requirements:
        results.append({
            "id": req.id,
            "text": req.text,
            "risk_type": req.risk_type.value if req.risk_type else None,
            "jurisdiction": req.jurisdiction,
            "page": req.page,
            "line": req.line,
            "short_description": random.choice(SUGGESTED_SENTENCES)
        })

    return {
        "count": len(results),
        "items": results
    }


# ------------------------------------------------------------
# GET /api/v1/requirements/suggested
# Random sample of requirements for “Recommended rules”
# ------------------------------------------------------------
@router.get("/suggested")
def suggested_requirements(
    limit: int = 5,
    jurisdiction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Returns a few randomly selected requirements to serve as
    'Suggested regulations'.
    """

    query = db.query(Requirement)

    if jurisdiction:
        query = query.filter(Requirement.jurisdiction == jurisdiction)

    all_requirements = query.all()

    if not all_requirements:
        return {"count": 0, "items": []}

    sample = random.sample(all_requirements, min(limit, len(all_requirements)))

    items = []
    for req in sample:
        items.append({
            "id": req.id,
            "text": req.text,
            "risk_type": req.risk_type.value,
            "jurisdiction": req.jurisdiction,
            "page": req.page,
            "line": req.line,
            "short_description": random.choice(SUGGESTED_SENTENCES)
        })

    return {
        "count": len(items),
        "items": items
    }


# ------------------------------------------------------------
# GET /api/v1/requirements/{id}
# Single requirement detail
# ------------------------------------------------------------
@router.get("/{requirement_id}")
def get_requirement(requirement_id: int, db: Session = Depends(get_db)):
    """
    Returns complete data for one requirement.
    """
    req = db.query(Requirement).filter(Requirement.id == requirement_id).first()

    if not req:
        return {"error": "Requirement not found"}

    return {
        "id": req.id,
        "text": req.text,
        "risk_type": req.risk_type.value if req.risk_type else None,
        "jurisdiction": req.jurisdiction,
        "page": req.page,
        "line": req.line,
        "description": random.choice(SUGGESTED_SENTENCES)
    }
