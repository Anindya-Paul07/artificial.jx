import ast
import os
import subprocess
import json
import re
from typing import Dict, List, Any, Tuple
from utils.helpers import load_json, save_json
from inference.groq_client import query_llama

ERROR_CACHE_PATH = "core/knowledge_base/error_solutions.json"
METADATA_PATH = "core/code_metadata.json"

class PythonErrorDetector:
    @staticmethod
    def detect_syntax_errors(code: str, file_path: str) -> List[Dict[str, Any]]:
        """Detect Python syntax errors using ast parser"""
        errors = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append({
                "type": "syntax",
                "line": e.lineno,
                "column": e.offset,
                "message": str(e),
                "severity": "error"
            })
        return errors
    
    @staticmethod
    def run_pylint(file_path: str) -> List[Dict[str, Any]]:
        """Run pylint on the file and parse results"""
        errors = []
        try:
            result = subprocess.run(
                ["pylint", "--output-format=json", file_path],
                capture_output=True,
                text=True
            )
            if result.stdout:
                pylint_issues = json.loads(result.stdout)
                for issue in pylint_issues:
                    errors.append({
                        "type": "linting",
                        "line": issue["line"],
                        "column": issue["column"],
                        "message": issue["message"],
                        "code": issue["symbol"],
                        "severity": map_pylint_severity(issue["type"])
                    })
        except Exception as e:
            print(f"[Junior] Error running pylint: {e}")
        return errors

    @staticmethod
    def check_common_mistakes(code: str) -> List[Dict[str, Any]]:
        """Check for common Python coding mistakes"""
        errors = []
        
        # Check for unused imports
        try:
            tree = ast.parse(code)
            imports = {node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)}
            names_used = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
            
            for imp in imports:
                # Simple check - doesn't handle from ... import ...
                if imp not in names_used:
                    errors.append({
                        "type": "logical",
                        "message": f"Unused import: {imp}",
                        "severity": "warning"
                    })
        except Exception as e:
            print(f"[Junior] Error checking for common mistakes: {e}")
            
        # Check for common anti-patterns
        patterns = [
            (r"except\s*:", "Bare except clause", "warning"),
            (r"except\s+Exception\s*:", "Too broad exception clause", "info"),
            (r"print\s*\(", "Print statement in production code", "info"),
            (r"\.sort\(\)\s*\.sort\(", "Double sorting", "warning"),
            (r"for\s+\w+\s+in\s+range\(len\((\w+)\)\):", "Using range(len()) instead of enumerate", "info"),
        ]
        
        for pattern, message, severity in patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                errors.append({
                    "type": "pattern",
                    "line": code[:match.start()].count('\n') + 1,
                    "message": message,
                    "severity": severity
                })
                
        return errors

def map_pylint_severity(sev_type: str) -> str:
    """Map pylint severity types to our standard"""
    mapping = {
        "error": "error",
        "warning": "warning",
        "convention": "info",
        "refactor": "info",
        "info": "info"
    }
    return mapping.get(sev_type, "info")

class JavaScriptErrorDetector:
    @staticmethod
    def detect_errors(code: str, file_path: str) -> List[Dict[str, Any]]:
        """Run ESLint on JavaScript files"""
        errors = []
        try:
            result = subprocess.run(
                ["npx", "eslint", "--format=json", file_path],
                capture_output=True,
                text=True
            )
            if result.stdout:
                eslint_results = json.loads(result.stdout)
                for file_result in eslint_results:
                    for message in file_result.get("messages", []):
                        errors.append({
                            "type": "linting",
                            "line": message.get("line", 0),
                            "column": message.get("column", 0),
                            "message": message.get("message", ""),
                            "code": message.get("ruleId", ""),
                            "severity": "error" if message.get("severity") == 2 else "warning"
                        })
        except Exception as e:
            print(f"[Junior] Error running ESLint: {e}")
        return errors

# Factory to get the appropriate detector
def get_detector(language: str):
    detectors = {
        "python": PythonErrorDetector,
        "javascript": JavaScriptErrorDetector,
        # Add more language detectors as implemented
    }
    return detectors.get(language)

def get_ai_suggestion(error: Dict[str, Any], code_context: str) -> str:
    """Get AI-powered suggestions for fixing an error"""
    # Check if we have a cached solution
    solutions = load_json(ERROR_CACHE_PATH)
    error_key = f"{error['type']}:{error.get('code', '')}:{error['message']}"
    
    if error_key in solutions:
        return solutions[error_key]
    
    # Generate suggestion using LLaMA
    prompt = f"""
    I have the following code error:
    Type: {error['type']}
    {f"Code: {error['code']}" if 'code' in error else ''}
    Message: {error['message']}
    
    Here is the context of the code:
    ```python
    {code_context}
    ```
    
    Please provide:
    1. A brief explanation of what's wrong
    2. A suggestion for how to fix it
    3. An example of the fixed code
    """
    
    suggestion = query_llama(prompt)
    
    # Cache the solution
    if suggestion:
        solutions[error_key] = suggestion
        save_json(ERROR_CACHE_PATH, solutions)
    
    return suggestion

def get_code_context(code: str, line_number: int, context_lines: int = 3) -> str:
    """Extract code context around the error line"""
    if not line_number:
        return code[:500]  # Return first 500 chars if no line number
        
    lines = code.split('\n')
    if line_number > len(lines):
        return code[:500]
        
    start = max(0, line_number - context_lines - 1)
    end = min(len(lines), line_number + context_lines)
    
    return '\n'.join(lines[start:end])

def analyze_file_for_errors(file_path: str) -> Dict[str, Any]:
    """Main function to analyze a file for errors and generate suggestions"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            
        # Determine language
        _, ext = os.path.splitext(file_path)
        language = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            # Add more mappings as needed
        }.get(ext, "unknown")
        
        if language == "unknown":
            return {"errors": [], "suggestions": []}
            
        # Get appropriate detector
        detector_class = get_detector(language)
        if not detector_class:
            return {"errors": [], "suggestions": []}
            
        errors = []
        
        # Collect errors from different detection methods
        if language == "python":
            errors.extend(detector_class.detect_syntax_errors(code, file_path))
            errors.extend(detector_class.check_common_mistakes(code))
            # Only run pylint if it's installed
            try:
                import pylint
                errors.extend(detector_class.run_pylint(file_path))
            except ImportError:
                pass
        elif language == "javascript":
            errors.extend(detector_class.detect_errors(code, file_path))
            
        # Generate suggestions for each error
        suggestions = []
        for error in errors:
            if error.get("line"):
                context = get_code_context(code, error["line"])
            else:
                context = code[:500]  # Use first 500 chars if no line number
                
            suggestion = get_ai_suggestion(error, context)
            if suggestion:
                suggestions.append({
                    "error": error,
                    "suggestion": suggestion
                })
                
        return {
            "file": file_path,
            "language": language,
            "errors": errors,
            "suggestions": suggestions
        }
                
    except Exception as e:
        print(f"[Junior] Error analyzing file: {e}")
        return {"errors": [], "suggestions": []}

# Initialize error cache if it doesn't exist
if not os.path.exists(ERROR_CACHE_PATH):
    os.makedirs(os.path.dirname(ERROR_CACHE_PATH), exist_ok=True)
    save_json(ERROR_CACHE_PATH, {})