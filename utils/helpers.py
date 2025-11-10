import json
import os

def load_config():
    """Reads the configuration file and returns a dict"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "config.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)