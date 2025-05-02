import json
import os
import ast

def detect_language(file_path):
    ext = os.path.splitext(file_path)[1]
    return {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".cpp": "cpp",
    }.get(ext, "unknown")

def extract_python_metadata(code):
    try:
        tree = ast.parse(code)
        imports = [node.names[0].name for node in tree.body if isinstance(node, ast.Import)]
        funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        summary = f"Imports: {', '.join(imports)}; Functions: {', '.join(funcs)}; Classes: {', '.join(classes)}"
        return summary
    except Exception as e:
        return f"Could not parse Python code: {e}"
def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
    
def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        