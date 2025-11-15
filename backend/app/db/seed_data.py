# app/db/seed_data.py

import random
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Requirement, RiskTypeEnum

# --- 1) Jurisdicciones simuladas ---
JURISDICTIONS = [
    "EU",
    "ESMA",
    "EBA",
    "ECB",
    "Basel",
    "UK-FCA",
    "FinCEN",
    "GLOBAL"
]

# --- 2) Mock Requirements profesionales ---
MOCK_REQUIREMENTS = [
    ("Institutions must implement robust client onboarding procedures including identity verification.", RiskTypeEnum.AML),
    ("Firms must detect, prevent, and report fraudulent transactions in real-time when feasible.", RiskTypeEnum.FRAUD),
    ("Entities must maintain cybersecurity controls preventing unauthorized access and data exfiltration.", RiskTypeEnum.CYBERSECURITY),
    ("Boards must maintain an independent risk committee overseeing internal control frameworks.", RiskTypeEnum.GOVERNANCE),
    ("Personal data must be processed lawfully and transparently, in line with GDPR Article 5.", RiskTypeEnum.PRIVACY),
    ("Firms must establish and test business continuity and contingency plans annually.", RiskTypeEnum.OPERATIONAL),
    ("Obliged entities must adhere to relevant regulatory technical standards and reporting obligations.", RiskTypeEnum.COMPLIANCE),
    ("Requirements that do not easily fit another category.", RiskTypeEnum.OTHER),
]

# Duplicate to create ~80 entries
MOCK_DATASET = [
    (text, cat, random.choice(JURISDICTIONS))
    for text, cat in MOCK_REQUIREMENTS
    for _ in range(10)
]


def seed():
    print("🌱 Seeding database with mock requirements...")

    db: Session = SessionLocal()

    # --- Insert requirements ---
    print("→ Adding mock requirements...")
    for idx, (text, risk, jur) in enumerate(MOCK_DATASET, start=1):
        db.add(
            Requirement(
                text=text,
                risk_type=risk,
                jurisdiction=jur
            )
        )
        if idx % 20 == 0:
            print(f"   Inserted {idx} requirements...")

    db.commit()
    db.close()

    print("🎉 DONE! Database successfully seeded.")


if __name__ == "__main__":
    seed()
