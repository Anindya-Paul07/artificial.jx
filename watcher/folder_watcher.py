import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from core.context_manager import analyze_file_event

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_types):
        self.file_types = file_types

    def on_modified(self, event):
        if event.is_directory:
            return
        _, ext = os.path.splitext(event.src_path)
        if ext in self.file_types:
            analyze_file_event(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        _, ext = os.path.splitext(event.src_path)
        if ext in self.file_types:
            analyze_file_event(event.src_path)

def start_watch(paths, file_types):
    event_handler = FileChangeHandler(file_types)
    observer = Observer()
    for path in paths:
        observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print(f"[Junior] Wacthing folders: {paths}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()