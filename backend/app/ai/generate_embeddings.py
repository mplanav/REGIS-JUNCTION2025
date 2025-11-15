# app/ai/generate_embeddings.py

import json
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer

from app.db.database import SessionLocal
from app.db.models import Requirement, RequirementEmbedding

# Load local embedding model
model = SentenceTransformer("intfloat/e5-base-v2")


def generate_embeddings():
    print("Generating embeddings locally with e5-base-v2…")

    db: Session = SessionLocal()
    requirements = db.query(Requirement).all()

    for req in requirements:
        exists = db.query(RequirementEmbedding).filter_by(requirement_id=req.id).first()
        if exists:
            continue

        # compute embedding
        emb = model.encode(req.text).tolist()

        db.add(
            RequirementEmbedding(
                requirement_id=req.id,
                embedding=json.dumps(emb)
            )
        )

        print(f"[{req.id}] Embedded.")

    db.commit()
    db.close()

    print("DONE.")


if __name__ == "__main__":
    generate_embeddings()
