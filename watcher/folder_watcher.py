import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import threading
from queue import Queue
from core.context_manager import analyze_file_event
from core.error_detector import analyze_file_for_errors
from core.ai_analyzer import ai_analyzer
from utils.helpers import load_json, save_json

# Path to store error analysis results
ERROR_ANALYSIS_PATH = "core/error_analysis.json"
ANALYSIS_QUEUE_PATH = "core/analysis_queue.json"

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_types):
        self.file_types = file_types
        self.analysis_queue = Queue()
        self.analysis_thread = threading.Thread(target=self._process_analysis_queue)
        self.analysis_thread.daemon = True
        self.analysis_thread.start()
        
        # Ensure error analysis file exists
        if not os.path.exists(ERROR_ANALYSIS_PATH):
            os.makedirs(os.path.dirname(ERROR_ANALYSIS_PATH), exist_ok=True)
            save_json(ERROR_ANALYSIS_PATH, {})
            
        # Load existing analysis queue
        self._load_analysis_queue()

    def _load_analysis_queue(self):
        """Load existing analysis queue from disk"""
        try:
            queue_data = load_json(ANALYSIS_QUEUE_PATH, default={})
            for file_path, timestamp in queue_data.items():
                if os.path.exists(file_path):
                    self.analysis_queue.put((file_path, timestamp))
        except Exception as e:
            print(f"Error loading analysis queue: {e}")

    def _save_analysis_queue(self):
        """Save current analysis queue to disk"""
        try:
            queue_data = {}
            for item in list(self.analysis_queue.queue):
                queue_data[item[0]] = item[1]
            save_json(ANALYSIS_QUEUE_PATH, queue_data)
        except Exception as e:
            print(f"Error saving analysis queue: {e}")

    def _process_analysis_queue(self):
        """Process files in the analysis queue"""
        while True:
            try:
                file_path, timestamp = self.analysis_queue.get()
                self._analyze_file(file_path)
                self.analysis_queue.task_done()
            except Exception as e:
                print(f"Error processing file: {e}")

    def _analyze_file(self, file_path):
        """Analyze a single file"""
        try:
            # Read file content
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Run syntax and linting checks
            error_results = analyze_file_for_errors(file_path)
            
            # Run AI analysis
            ai_analysis = ai_analyzer.analyze_code(content, file_path)
            
            # Combine results
            analysis_data = {
                "timestamp": time.time(),
                "syntax_errors": error_results.get("errors", []),
                "linting_issues": error_results.get("suggestions", []),
                "ai_analysis": ai_analysis
            }
            
            # Save results
            error_data = load_json(ERROR_ANALYSIS_PATH)
            error_data[file_path] = analysis_data
            save_json(ERROR_ANALYSIS_PATH, error_data)
            
            print(f"[Junior] Completed analysis for {file_path}")
            
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")

    def on_modified(self, event):
        if event.is_directory:
            return
        _, ext = os.path.splitext(event.src_path)
        if ext in self.file_types:
            self._queue_file(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        _, ext = os.path.splitext(event.src_path)
        if ext in self.file_types:
            self._queue_file(event.src_path)

    def _queue_file(self, file_path):
        """Add file to analysis queue"""
        try:
            # Only add if file exists and is not already in queue
            if os.path.exists(file_path):
                self.analysis_queue.put((file_path, time.time()))
                self._save_analysis_queue()
                print(f"[Junior] Queued analysis for {file_path}")
        except Exception as e:
            print(f"Error queuing file: {e}")
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