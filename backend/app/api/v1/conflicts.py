from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
import random

from app.db.database import get_db
from app.db.models.requirements import Requirement
from app.db.models.requirements import Contradiction, Overlap

router = APIRouter(prefix="/conflicts", tags=["Conflicts"])


# ------------------------------------------------------------
# Simulated descriptions
# ------------------------------------------------------------

CONTRADICTION_SENTENCES = [
    "These requirements conflict in scope and compliance interpretation.",
    "The obligations contradict due to incompatible regulatory thresholds.",
    "There is a legal contradiction between applicability conditions.",
    "Operational limits in one rule invalidate obligations in the other.",
    "Interpretation mismatch: requirement A restricts what B mandates.",
]

OVERLAP_SENTENCES = [
    "These requirements cover the same operational scope.",
    "The rules are duplicates with slight wording differences.",
    "Both obligations demand nearly identical compliance actions.",
    "Overlap detected: same policy requirement expressed twice.",
    "Redundant guidance: both regulate the same underlying process."
]


# ------------------------------------------------------------
# GET /api/v1/conflicts/summary
# Used for the pie/donut chart (contradictions vs overlaps)
# ------------------------------------------------------------
@router.get("/summary")
def conflicts_summary(
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction"),
    db: Session = Depends(get_db)
):
    """
    Returns the count and percentage of contradictions and overlaps.
    Used for the conflict chart.
    """
    # Base queries
    contradictions_query = db.query(Contradiction)
    overlaps_query = db.query(Overlap)

    if jurisdiction:
        contradictions_query = contradictions_query.filter(Contradiction.jurisdiction == jurisdiction)
        overlaps_query = overlaps_query.filter(Overlap.jurisdiction == jurisdiction)

    contradictions = contradictions_query.count()
    overlaps = overlaps_query.count()

    total = contradictions + overlaps

    if total == 0:
        return {
            "total": 0,
            "items": []
        }

    return {
        "total": total,
        "items": [
            {
                "type": "contradiction",
                "count": contradictions,
                "percentage": round((contradictions / total) * 100, 2),
                "description": "Cases where two requirements conflict or impose opposing obligations."
            },
            {
                "type": "overlap",
                "count": overlaps,
                "percentage": round((overlaps / total) * 100, 2),
                "description": "Cases where two requirements are redundant or partially duplicate."
            }
        ]
    }


# ------------------------------------------------------------
# GET /api/v1/conflicts/detail/{conflict_type}
# Returns individual contradictions or overlaps
# ------------------------------------------------------------
@router.get("/detail/{conflict_type}")
def conflicts_detail(
    conflict_type: str,
    jurisdiction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Return the list of contradictions OR overlaps, including:
    - IDs
    - related requirement texts
    - pages/lines
    - simulated explanation text
    """
    if conflict_type not in ["contradiction", "overlap"]:
        return {"error": "Invalid conflict type. Use 'contradiction' or 'overlap'."}

    if conflict_type == "contradiction":
        query = db.query(Contradiction)
    else:
        query = db.query(Overlap)

    if jurisdiction:
        query = query.filter(
            Contradiction.jurisdiction == jurisdiction if conflict_type == "contradiction"
            else Overlap.jurisdiction == jurisdiction
        )

    results = query.all()

    response_items = []
    for item in results:

        # Fetch related requirements
        req1 = db.query(Requirement).filter(Requirement.id == item.requirement1_id).first()
        req2 = db.query(Requirement).filter(Requirement.id == item.requirement2_id).first()

        response_items.append({
            "id": item.id,
            "type": conflict_type,
            "jurisdiction": item.jurisdiction,
            "description": (
                item.description
                if conflict_type == "contradiction"
                else item.reason
            ),
            "requirement_1": {
                "id": req1.id,
                "text": req1.text,
                "page": req1.page,
                "line": req1.line,
                "jurisdiction": req1.jurisdiction
            },
            "requirement_2": {
                "id": req2.id,
                "text": req2.text,
                "page": req2.page,
                "line": req2.line,
                "jurisdiction": req2.jurisdiction
            }
        })

    return {
        "count": len(results),
        "type": conflict_type,
        "items": response_items
    }
