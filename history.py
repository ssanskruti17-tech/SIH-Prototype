import os
import json
from datetime import datetime

HISTORY_DIR = "history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")


def initialize_history():
    os.makedirs(HISTORY_DIR, exist_ok=True)

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as file:
            json.dump([], file)


def load_history():
    initialize_history()

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except:
        return []


def save_scan(scan_data):
    initialize_history()

    history = load_history()

    history.insert(0, scan_data)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def create_scan_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")