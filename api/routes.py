from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Junior FastAPI is running!"}

@router.get("/status")
def get_status():
    return {"status":"running", "message":"Junior backend is active."}

@router.post("/analyze")
def trigger_analysis():
    from core.doc_suggester import analyze_
    return{"message":"Manual analysis triggered (to be implemented)."}