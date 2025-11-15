# app/ai/classify_risks_with_fireworks.py

import os
import requests
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Requirement

API_KEY = os.getenv("FIREWORKS_API_KEY")
CHAT_URL = os.getenv("FIREWORKS_CHAT_URL", "https://api.fireworks.ai/v1/chat/completions")

MODEL = "accounts/fireworks/models/llama-v3p1-70b-instruct"

RISK_TYPES = [
    "AML", "FRAUD", "CYBERSECURITY", "GOVERNANCE",
    "PRIVACY", "OPERATIONAL", "COMPLIANCE", "OTHER"
]


def classify(text: str) -> str:
    prompt = f"""
    Classify the following regulatory requirement into exactly ONE risk category:
    {", ".join(RISK_TYPES)}.

    Requirement:
    \"\"\"{text}\"\"\"

    Respond with only the category, nothing else.
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    r = requests.post(CHAT_URL, json=payload, headers=headers)
    r.raise_for_status()

    output = r.json()["choices"][0]["message"]["content"].strip()

    return output if output in RISK_TYPES else "OTHER"


def classify_all():
    print("Classifying risks using Fireworks…")

    db: Session = SessionLocal()
    reqs = db.query(Requirement).all()

    for req in reqs:
        label = classify(req.text)
        req.risk_type = label
        print(f"[{req.id}] → {label}")

    db.commit()
    db.close()
    print("Risk classification completed.")


if __name__ == "__main__":
    classify_all()
