import os
import zipfile
import json
from datetime import datetime

from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.models.document import Document, CategoryLevel, DocumentType
from db.models.chunk import Chunk

from ingestion.xml_parser import parse_xml_into_chunks
from ingestion.text_utils import clean_text

# --- CONFIG ---
DATA_DIR = "/data"  # Mounted via docker-compose
ZIP_FILE_TO_PROCESS = "gold.zip"
CATEGORY = CategoryLevel.gold
DOC_TYPE = DocumentType.financial_regulation  # adjust dynamically later
# ---------------


def flatten_json_file(file_bytes):
    """
    Convert a JSON file (pages + paragraphs) into a list of chunks.
    Expects format:
    {
        "pages": [
            {
                "page": 1,
                "paragraphs": ["text 1", "text 2", ...]
            },
            ...
        ]
    }
    """
    chunks = []

    try:
        data = json.loads(file_bytes)
        for page in data.get("pages", []):
            page_num = page.get("page")

            for para in page.get("paragraphs", []):
                text = clean_text(para or "")
                if not text:
                    continue

                chunks.append({
                    "text": text,
                    "article_ref": f"page_{page_num}",
                })

    except Exception as e:
        print(f"[ERROR] JSON parse failed: {e}")

    return chunks


def process_one_file(filename: str, file_bytes: bytes, db: Session, category=CATEGORY):
    """
    Decide if file is JSON/XML, parse it, create document + chunks.
    """

    # Skip obviously binary/corrupted files
    if b"\x00" in file_bytes[:200]:
        print(f"  [SKIP] Binary/corrupted file: {filename}")
        return

    print(f" → Processing file: {filename}")

    # 1) Create the Document row
    document = Document(
        file_path=os.path.join(DATA_DIR, ZIP_FILE_TO_PROCESS, filename),
        title=None,
        jurisdiction=None,
        category_level=category,
        doc_type=DOC_TYPE,
        created_at=datetime.utcnow(),
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # 2) Extract chunks
    if filename.endswith(".json"):
        chunks_data = flatten_json_file(file_bytes)
    elif filename.endswith(".xml"):
        chunks_data = parse_xml_into_chunks(file_bytes)
    else:
        print(f"  [SKIP] Unsupported file type: {filename}")
        return

    if not chunks_data:
        print(f"  [WARN] No chunks extracted for {filename}")
        return

    # 3) Insert chunks into DB
    for c in chunks_data:
        chunk = Chunk(
            document_id=document.id,
            text=clean_text(c.get("text", "")),
            article_ref=clean_text(c.get("article_ref", "")) or None,
            embedding=None,
            risk_labels=None,
        )
        db.add(chunk)

    db.commit()
    print(f"   Inserted {len(chunks_data)} chunks.")


def main():
    print(f"Starting ingestion for {ZIP_FILE_TO_PROCESS}")

    db = SessionLocal()

    zip_path = os.path.join(DATA_DIR, ZIP_FILE_TO_PROCESS)
    if not os.path.exists(zip_path):
        print(f"FATAL: ZIP not found at {zip_path}")
        return

    with zipfile.ZipFile(zip_path, "r") as zf:
        file_list = zf.namelist()
        total_files = len(file_list)

        print(f"Found {total_files} files in {ZIP_FILE_TO_PROCESS}")

        for i, filename in enumerate(file_list):
            # Skip directories and macOS junk
            if filename.endswith("/") or "__MACOSX" in filename:
                continue

            if not (filename.endswith(".xml") or filename.endswith(".json")):
                continue

            if i % 100 == 0:
                print(f"  ...{i}/{total_files} files processed")

            with zf.open(filename) as f:
                file_bytes = f.read()
                if not file_bytes:
                    continue

                try:
                    process_one_file(filename, file_bytes, db)
                except Exception as e:
                    print(f"[ERROR] Failed on file {filename}: {e}")

    print("Ingestion Complete — Silver layer stored in PostgreSQL!")


if __name__ == "__main__":
    main()
