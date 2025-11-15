# app/ai/classify_risks_heuristic.py

import re
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Requirement


# --- Define risk categories and keywords ---
RISK_KEYWORDS = {
    "AML": [
        r"\banti[- ]?money[- ]?laundering\b",
        r"\baml\b",
        r"\bmoney laundering\b",
        r"\bterrorist financing\b",
        r"\bml\/tf\b",
        r"\bknow your customer\b",
        r"\bkYC\b",
        r"\bcustomer due diligence\b",
    ],
    "FRAUD": [
        r"\bfraud\b",
        r"\bfraudulent\b",
        r"\bmisrepresentation\b",
        r"\bscam\b",
        r"\bembezzlement\b",
    ],
    "CYBERSECURITY": [
        r"\bcyber\b",
        r"\bit security\b",
        r"\bsecurity breach\b",
        r"\binformation security\b",
        r"\bcybersecurity\b",
        r"\bencryption\b",
        r"\battack\b",
        r"\bhacking\b",
    ],
    "GOVERNANCE": [
        r"\bgovenance\b",
        r"\bboard\b",
        r"\bcommittee\b",
        r"\bmanagement body\b",
        r"\binternal control\b",
        r"\brisk management\b",
    ],
    "PRIVACY": [
        r"\bprivacy\b",
        r"\bdata protection\b",
        r"\bGDPR\b",
        r"\bpersonal data\b",
        r"\bdata subject\b",
    ],
    "OPERATIONAL": [
        r"\boperational risk\b",
        r"\boutsourcing\b",
        r"\bthird[- ]party\b",
        r"\bbusiness continuity\b",
        r"\bBCP\b",
        r"\bcontingency\b",
        r"\bprocess\b",
    ],
    "COMPLIANCE": [
        r"\bcompliance\b",
        r"\blegal obligation\b",
        r"\bregulatory\b",
        r"\bregulation\b",
    ]
}

DEFAULT_CATEGORY = "OTHER"


def classify_text(text: str) -> str:
    text = text.lower()

    for category, patterns in RISK_KEYWORDS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return category

    return DEFAULT_CATEGORY


def classify_all():
    print("Classifying risks using heuristics…")

    db: Session = SessionLocal()
    requirements = db.query(Requirement).all()

    for r in requirements:
        label = classify_text(r.text)
        r.risk_type = label
        print(f"[{r.id}] → {label}")

    db.commit()
    db.close()

    print("Heuristic classification complete.")


if __name__ == "__main__":
    classify_all()
