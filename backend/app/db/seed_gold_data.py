import random
import json
from datetime import datetime

from sqlalchemy.orm import Session

# IMPORTS CORRECTOS
from app.db.database import engine, Base
from app.db.models.document import Document, CategoryLevel, DocumentType
from app.db.models.requirements import (
    Requirement, RequirementEmbedding,
    Contradiction, Overlap,
    RiskTypeEnum
)

# =====================================
#   CONFIGURACIÓN DEL SEED
# =====================================

FAKE_JURISDICTIONS = ["EU", "FINLAND", "GLOBAL"]
FAKE_TITLES = [
    "EU Capital Requirements Regulation",
    "Finnish Mortgage Credit Act",
    "Basel Governance Framework",
    "MiFID II Conduct Requirements",
]

FAKE_RISK_TYPES = list(RiskTypeEnum)

FAKE_SENTENCES = [
    "The institution shall maintain adequate internal controls.",
    "Risk exposure must be monitored on an ongoing basis.",
    "Liquidity buffers shall be calibrated to withstand stress scenarios.",
    "Credit policies must define approval thresholds and documentation requirements.",
    "Institutions shall establish cyber incident detection capabilities.",
    "Adequate governance arrangements must be in place.",
    "Data protection obligations apply to all customer information processing.",
]


def fake_embedding(dim=1536):
    """Generate a fake embedding vector with random floats."""
    return [round(random.uniform(-1, 1), 5) for _ in range(dim)]


def seed_database():

    # Reset de la BDD (DROP + CREATE)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = Session(bind=engine)
    print("⏳ Seeding database with random variation...")

    # ------------------------------------------------------
    # 1. DOCUMENTOS
    # ------------------------------------------------------
    documents = []
    for i in range(4):
        doc = Document(
            file_path=f"/data/fake_doc_{i}.xml",
            title=random.choice(FAKE_TITLES),
            jurisdiction=random.choice(FAKE_JURISDICTIONS),
            category_level=CategoryLevel.gold,
            doc_type=DocumentType.financial_regulation,
            created_at=datetime.utcnow(),
        )
        session.add(doc)
        documents.append(doc)

    session.commit()

    # ------------------------------------------------------
    # 2. REQUIREMENTS (80)
    # ------------------------------------------------------
    requirements = []
    for i in range(80):

        parent_doc = random.choice(documents)

        req = Requirement(
            text=random.choice(FAKE_SENTENCES),
            page=random.randint(1, 25),
            line=random.randint(1, 60),
            risk_type=random.choice(FAKE_RISK_TYPES),
            jurisdiction=random.choice(FAKE_JURISDICTIONS),
            document_id=parent_doc.id  # RELACIÓN REAL
        )

        session.add(req)
        session.flush()

        emb = RequirementEmbedding(
            requirement_id=req.id,
            embedding=json.dumps(fake_embedding())
        )
        session.add(emb)

        requirements.append(req)

    session.commit()

    # ------------------------------------------------------
    # 3. OVERLAPS & CONTRADICTIONS
    # ------------------------------------------------------

    NUM_OVERLAPS = random.randint(20, 70)
    NUM_CONTRADICTIONS = random.randint(25, 60)

    print(f"📊 Creating {NUM_OVERLAPS} overlaps")
    print(f"⚠️ Creating {NUM_CONTRADICTIONS} contradictions")

    def pick_two():
        return random.sample(requirements, 2)

    # OVERLAPS
    for _ in range(NUM_OVERLAPS):
        r1, r2 = pick_two()
        session.add(Overlap(
            requirement1_id=r1.id,
            requirement2_id=r2.id,
            reason="Overlapping regulatory requirement detected.",
            page_1=r1.page,
            line_1=r1.line,
            page_2=r2.page,
            line_2=r2.line,
            jurisdiction=random.choice(FAKE_JURISDICTIONS),
        ))

    # CONTRADICTIONS
    for _ in range(NUM_CONTRADICTIONS):
        r1, r2 = pick_two()
        session.add(Contradiction(
            requirement1_id=r1.id,
            requirement2_id=r2.id,
            description="Conflicting threshold or incompatible timeline.",
            page_1=r1.page,
            line_1=r1.line,
            page_2=r2.page,
            line_2=r2.line,
            jurisdiction=random.choice(FAKE_JURISDICTIONS),
        ))

    session.commit()
    session.close()

    print("✅ Database seeded successfully with random variability.")


if __name__ == "__main__":
    seed_database()
