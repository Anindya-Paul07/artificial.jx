from watcher.folder_watcher import start_watch
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        # Normalize config keys
        if "file_type" in config and "file_types" not in config:
            config["file_types"] = config["file_type"]
        return config
    
if __name__ == "__main__":
    config = load_config()
    watch_paths = config.get("watch_paths", [])
    file_types = config.get("file_types", [])
    start_watch(watch_paths, file_types)