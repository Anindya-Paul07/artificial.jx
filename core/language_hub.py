import os
from typing import Dict, Any, List
import importlib
from utils.helpers import load_json, save_json

# Path to store language-specific handlers and plugins
LANGUAGE_HUB_PATH = "core/language_hub"
LANGUAGE_CONFIG_PATH = "core/language_hub/config.json"

class LanguageHub:
    """Central hub for managing language-specific processing modules"""
    
    def __init__(self):
        self._ensure_dirs()
        self.config = self._load_config()
        self.language_modules = {}
        self._load_registered_modules()
        
    def _ensure_dirs(self):
        """Ensure necessary directories exist"""
        os.makedirs(LANGUAGE_HUB_PATH, exist_ok=True)
        
        # Create __init__.py to make it a proper package
        init_path = os.path.join(LANGUAGE_HUB_PATH, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w") as f:
                f.write("# Language Hub Package\n")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load language hub configuration"""
        if os.path.exists(LANGUAGE_CONFIG_PATH):
            return load_json(LANGUAGE_CONFIG_PATH)
        else:
            # Initialize with default configuration
            default_config = {
                "registered_languages": {
                    "python": {
                        "extensions": [".py"],
                        "module": "python_handler",
                        "enabled": True
                    },
                    "javascript": {
                        "extensions": [".js"],
                        "module": "javascript_handler",
                        "enabled": True
                    },
                    "typescript": {
                        "extensions": [".ts"],
                        "module": "typescript_handler",
                        "enabled": True
                    }
                },
                "default_handlers": {
                    "error_detection": True,
                    "code_completion": False,
                    "refactoring": False
                }
            }
            save_json(LANGUAGE_CONFIG_PATH, default_config)
            return default_config
    
    def _load_registered_modules(self):
        """Load all registered language modules"""
        for lang, config in self.config["registered_languages"].items():
            if config["enabled"]:
                try:
                    # Try to dynamically import the module
                    module_path = f"core.language_hub.{config['module']}"
                    module = importlib.import_module(module_path)
                    self.language_modules[lang] = module
                    print(f"[Junior] Loaded language module for {lang}")
                except ImportError:
                    print(f"[Junior] Language module for {lang} not found, will be created on demand")
    
    def get_handler_for_language(self, language: str):
        """Get the appropriate handler for a language"""
        if language in self.language_modules:
            return self.language_modules[language]
        
        # If module doesn't exist but is registered, create a skeleton
        if language in self.config["registered_languages"]:
            self._create_skeleton_module(language)
            return self.language_modules.get(language)
            
        return None
    
    def get_language_by_extension(self, file_extension: str) -> str:
        """Determine language from file extension"""
        for lang, config in self.config["registered_languages"].items():
            if file_extension in config["extensions"]:
                return lang
        return "unknown"
    
    def _create_skeleton_module(self, language: str):
        """Create a skeleton module for a language if it doesn't exist"""
        config = self.config["registered_languages"][language]
        module_name = config["module"]
        file_path = os.path.join(LANGUAGE_HUB_PATH, f"{module_name}.py")
        
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(f"""# {language.capitalize()} Language Handler
from typing import Dict, List, Any

class {language.capitalize()}Handler:
    \"\"\"Handler for {language} code analysis\"\"\"
    
    @staticmethod
    def detect_errors(code: str, file_path: str) -> List[Dict[str, Any]]:
        \"\"\"Detect errors in {language} code\"\"\"
        # Placeholder implementation
        return []
    
    @staticmethod
    def suggest_fixes(errors: List[Dict[str, Any]], code: str) -> List[Dict[str, Any]]:
        \"\"\"Generate fix suggestions for {language} errors\"\"\"
        # Placeholder implementation
        return []
    
    @staticmethod
    def analyze_code_quality(code: str) -> Dict[str, Any]:
        \"\"\"Analyze code quality metrics for {language}\"\"\"
        # Placeholder implementation
        return {{
            "complexity": 0,
            "maintainability": 0,
            "documentation": 0
        }}

# Export the handler
handler = {language.capitalize()}Handler()
""")
            
            # Make sure we have an updated __init__.py that imports this module
            init_path = os.path.join(LANGUAGE_HUB_PATH, "__init__.py")
            with open(init_path, "a") as f:
                f.write(f"from .{module_name} import handler as {language}_handler\n")
            
            # Try to import the newly created module
            try:
                module_path = f"core.language_hub.{module_name}"
                self.language_modules[language] = importlib.import_module(module_path)
                print(f"[Junior] Created and loaded skeleton module for {language}")
            except ImportError as e:
                print(f"[Junior] Failed to load newly created module: {e}")

# Initialize the language hub
language_hub = LanguageHub()