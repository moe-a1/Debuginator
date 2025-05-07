import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config" / "config.json"

def load_config():
    if not CONFIG_FILE.exists():
        return {"api_key": "", "model": ""}
    
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=2)
