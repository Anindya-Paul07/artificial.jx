from watcher.folder_watcher import start_watch
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)
    
if __name__ == "__main__":
    config = load_config()
    watch_paths = config.get("watch_paths", [])
    file_types = config.get("file_types", [])
    start_watch(watch_paths, file_types)