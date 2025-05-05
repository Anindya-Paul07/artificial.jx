from fastapi import APIRouter
from core.doc_suggester import suggest_docs

router = APIRouter()

@router.get("/suggest-docs")
def suggest():
    suggestions = suggest_docs()
    return {"suggestions": suggestions}