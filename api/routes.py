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
    #logic will be added for UI-triggred scans
    return{"message":"Manual analysis triggered (to be implemented)."}