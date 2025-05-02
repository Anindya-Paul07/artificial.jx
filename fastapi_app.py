import yaml
import threading
from fastapi import FastAPI
from watcher.folder_watcher import start_watch
from api.routes import router as api_router

app = FastAPI()
app.include_router(api_router)

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)
    
def start_watcher_thread():
    config = load_config()
    watch_paths = config.get("watch_paths", [])
    file_types = config.get("file_types", [])
    watcher_thread = threading.Thread(target=start_watch, args=(watch_paths, file_types), daemon=True)
    watcher_thread.start()


@app.on_event("startup")
def on_startup():
    print("[Junior] Starting FastAPI app and folder watcher...")
    start_watcher_thread()
