# app/ai/detect_overlaps.py

import json
import numpy as np
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import RequirementEmbedding, Overlap

SIM_THRESHOLD = 0.82


def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def detect_overlaps():
    print("Detecting overlaps…")

    db: Session = SessionLocal()

    embeddings = db.query(RequirementEmbedding).all()
    vecs = {e.requirement_id: json.loads(e.embedding) for e in embeddings}

    ids = list(vecs.keys())

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            r1 = ids[i]
            r2 = ids[j]
            sim = cosine(vecs[r1], vecs[r2])

            if sim >= SIM_THRESHOLD:
                db.add(
                    Overlap(
                        requirement1_id=r1,
                        requirement2_id=r2,
                        reason=f"Similarity {sim:.2f}",
                        jurisdiction="GLOBAL"
                    )
                )
                print(f"Overlap: {r1} ↔ {r2} (sim={sim:.2f})")

    db.commit()
    db.close()
    print("Overlap detection complete.")


if __name__ == "__main__":
    detect_overlaps()
