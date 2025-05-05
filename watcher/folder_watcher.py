import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from core.context_manager import analyze_file_event
from core.error_detector import analyze_file_for_errors
from utils.helpers import load_json, save_json

# Path to store error analysis results
ERROR_ANALYSIS_PATH = "core/error_analysis.json"

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_types):
        self.file_types = file_types
        # Ensure error analysis file exists
        if not os.path.exists(ERROR_ANALYSIS_PATH):
            os.makedirs(os.path.dirname(ERROR_ANALYSIS_PATH), exist_ok=True)
            save_json(ERROR_ANALYSIS_PATH, {})

    def on_modified(self, event):
        if event.is_directory:
            return
        _, ext = os.path.splitext(event.src_path)
        if ext in self.file_types:
            # Run the existing context analysis
            analyze_file_event(event.src_path)
            
            # Add error detection
            self._handle_error_detection(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        _, ext = os.path.splitext(event.src_path)
        if ext in self.file_types:
            analyze_file_event(event.src_path)
            self._handle_error_detection(event.src_path)
            
    def _handle_error_detection(self, file_path):
        """Handle error detection for modified or created files"""
        print(f"[Junior] Running error detection on {file_path}")
        
        # Analyze file for errors
        error_results = analyze_file_for_errors(file_path)
        
        # Save error analysis to persistent store
        if error_results and (error_results.get("errors") or error_results.get("suggestions")):
            error_data = load_json(ERROR_ANALYSIS_PATH)
            error_data[file_path] = {
                "timestamp": time.time(),
                "results": error_results
            }
            save_json(ERROR_ANALYSIS_PATH, error_data)
            
            # Log results summary
            error_count = len(error_results.get("errors", []))
            suggestion_count = len(error_results.get("suggestions", []))
            print(f"[Junior] Found {error_count} errors and provided {suggestion_count} suggestions")
            
            # Print each error for quick reference
            for error in error_results.get("errors", []):
                severity = error.get("severity", "info").upper()
                message = error.get("message", "Unknown error")
                line = error.get("line", "?")
                print(f"[Junior] {severity} at line {line}: {message}")

def start_watch(paths, file_types):
    event_handler = FileChangeHandler(file_types)
    observer = Observer()
    for path in paths:
        observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print(f"[Junior] Watching folders: {paths}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()