from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
import random

from app.db.database import get_db
from app.db.models.requirements import Requirement, RiskTypeEnum

router = APIRouter(prefix="/risks", tags=["Risks"])


# ------------------------------------------------------------
# Helper: Simular descripciones de riesgo
# ------------------------------------------------------------

RISK_DESCRIPTIONS = {
    RiskTypeEnum.AML: "Anti-Money Laundering risks related to suspicious transactions and weak controls.",
    RiskTypeEnum.FRAUD: "Fraud risk related to misrepresentation, misuse of documents or intentional deception.",
    RiskTypeEnum.CYBERSECURITY: "Cybersecurity risks such as data breaches, malware, or unauthorized access.",
    RiskTypeEnum.GOVERNANCE: "Governance risks related to board oversight, accountability, and transparency.",
    RiskTypeEnum.PRIVACY: "Privacy risks connected to personal data misuse or GDPR-related violations.",
    RiskTypeEnum.OPERATIONAL: "Operational risks involving process failures, human errors or system breakdowns.",
    RiskTypeEnum.COMPLIANCE: "Regulatory or compliance risks due to violations of applicable laws or policies.",
    RiskTypeEnum.OTHER: "Miscellaneous risks that do not fall under standard categories."
}


# ------------------------------------------------------------
# GET /api/v1/risks/summary
# Summary for the bar chart
# ------------------------------------------------------------
@router.get("/summary")
def risk_summary(
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction (optional)"),
    db: Session = Depends(get_db)
):
    """
    Returns the count and percentage of each risk type.
    Used for the bar chart in the frontend.
    """
    query = db.query(Requirement)

    if jurisdiction:
        query = query.filter(Requirement.jurisdiction == jurisdiction)

    requirements = query.all()

    if not requirements:
        return {
            "total": 0,
            "risks": []
        }

    total = len(requirements)

    # Count each risk type
    counts: Dict[str, int] = {r.value: 0 for r in RiskTypeEnum}
    for req in requirements:
        counts[req.risk_type.value] += 1

    # Build response
    result = []
    for risk, count in counts.items():
        if count > 0:  # Only return risks that appear
            result.append({
                "risk_type": risk,
                "count": count,
                "percentage": round((count / total) * 100, 2),
                "description": RISK_DESCRIPTIONS.get(RiskTypeEnum(risk), "No description available.")
            })

    return {
        "total": total,
        "risks": result
    }


# ------------------------------------------------------------
# GET /api/v1/risks/detail/{risk_type}
# When clicking on the bar → show details
# ------------------------------------------------------------
@router.get("/detail/{risk_type}")
def risk_detail(
    risk_type: RiskTypeEnum,
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction"),
    db: Session = Depends(get_db)
):
    """
    Returns detailed requirements associated with a given risk type.
    Used when clicking a bar in the risk coverage chart.
    """
    query = db.query(Requirement).filter(Requirement.risk_type == risk_type)

    if jurisdiction:
        query = query.filter(Requirement.jurisdiction == jurisdiction)

    requirements = query.all()

    return {
        "risk_type": risk_type.value,
        "description": RISK_DESCRIPTIONS.get(risk_type, "No description available."),
        "count": len(requirements),
        "items": [
            {
                "id": req.id,
                "text": req.text,
                "page": req.page,
                "line": req.line,
                "jurisdiction": req.jurisdiction
            }
            for req in requirements
        ]
    }
