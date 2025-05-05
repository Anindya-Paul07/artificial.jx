from fastapi import APIRouter
from watcher.folder_watcher import start_watch
from pydantic import BaseModel


router = APIRouter()

class WatchRequest(BaseModel):
    paths: list[str]
    file_types: list[str]

@router.post("/start-watch")
def start_watcher(req: WatchRequest):
    start_watch(req.paths, req.file_types)
    return {"status": "Watcher started"}