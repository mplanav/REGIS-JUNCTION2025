from fastapi import APIRouter, HTTPException
from app.ai.document_mock_data import DOCUMENTS

router = APIRouter()

@router.get("/")
def list_documents():
    return DOCUMENTS


@router.get("/{doc_id}")
def get_document(doc_id: int):
    for doc in DOCUMENTS:
        if doc["id"] == doc_id:
            return doc
    raise HTTPException(status_code=404, detail="Document not found")


@router.get("/search/")
def search_documents(query: str):
    query = query.lower()
    results = [d for d in DOCUMENTS if query in d["title"].lower() or query in d["summary"].lower()]
    return results
