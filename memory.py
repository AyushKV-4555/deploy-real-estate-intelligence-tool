import json
import os


FILE = "job_memory.json"


def load_memory():
    if os.path.exists(FILE):
        with open(FILE, 'r') as f:
            return json.load(f)
    return {}


def save_memory(data):
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=2)