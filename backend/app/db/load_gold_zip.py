# app/db/load_gold_zip.py

import zipfile
import json
from pathlib import Path

from sqlalchemy.orm import Session

from .database import engine, SessionLocal, Base
from .models import Requirement


GOLD_ZIP_PATH = Path("gold.zip")


def load_basel_di_json(content: bytes, db: Session):
    """
    Carga un archivo tipo BaselFramework.di.json
    """
    data = json.loads(content.decode("utf-8"))
    pages = data.get("pages", [])
    inserted = 0

    for page_obj in pages:
        page_num = page_obj.get("page")
        paragraphs = page_obj.get("paragraphs", [])

        for idx, para in enumerate(paragraphs):
            text = (para or "").strip()
            if not text:
                continue
            if text.startswith("Downloaded on"):
                continue

            line_num = idx + 1

            req = Requirement(
                text=text,
                page=page_num,
                line=line_num,
                risk_type="OTHER",       # default provisional
                jurisdiction="GLOBAL",   # Basel es global
            )
            db.add(req)
            inserted += 1

    print(f"Inserted {inserted} requirements from Basel-style JSON")


def load_gold_data(db: Session):
    print("Creating tables if they do not exist...")
    Base.metadata.create_all(bind=engine)

    print("Loading gold.zip...")
    if not GOLD_ZIP_PATH.exists():
        print("ERROR: gold.zip not found!")
        return

    with zipfile.ZipFile(GOLD_ZIP_PATH, "r") as z:
        for filename in z.namelist():
            print(f"Processing: {filename}")

            # Todos los BaselFramework.di.json
            if filename.endswith(".di.json"):
                with z.open(filename) as f:
                    content = f.read()
                    load_basel_di_json(content, db)
                continue

            # Otros JSON (por ahora no se usan)
            if filename.endswith(".json"):
                print(f"Skipping JSON not in Basel format: {filename}")
                continue

            # XMLs son metadatos
            if filename.endswith(".xml"):
                print(f"Skipping XML metadata: {filename}")
                continue

            print(f"Skipping unsupported file: {filename}")

        db.commit()
        print("All requirements inserted.")

    print("DONE.")


if __name__ == "__main__":
    db = SessionLocal()
    load_gold_data(db)
    db.close()
