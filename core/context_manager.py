import os
import json
import ast
from sentence_transformers  import SentenceTransformer
from utils.helpers import detect_language, extract_python_metadata, load_json, save_json

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
METADATA_PATH = "core/code_metadata.json"

def analyze_file_event(file_path):
    print(f"[Junior] Detected change in {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        language = detect_language(file_path)
        metadata = {
            "file": file_path,
            "language": language,
            "summary": "",
            "embedding": [],
        }

        if language == "python":
            metadata["summary"] = extract_python_metadata(code)

        metadata["embedding"] = model.encode(metadata["summary"]).tolist()

        # Initialize metadata if file doesn't exist
        if not os.path.exists(METADATA_PATH):
            os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
            save_json(METADATA_PATH, {})
            
        all_meta = load_json(METADATA_PATH)
        all_meta[file_path] = metadata
        save_json(METADATA_PATH, all_meta)

        print(f"[Junior] Scanned {len(code)} characters of code")
    except Exception as e:
        print(f"[Junior] Error reading file: {e}")
