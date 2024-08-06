"""json file handlers."""

import json
from typing import Any


def save_to_json(data: Any, file_path: str):
    """save to json."""
    with open(file_path, "w", encoding="utf-8") as write_file:
        json.dump(data, write_file)


def load_from_json(file_path: str):
    """load from json."""
    try:
        with open(file_path, "r", encoding="utf-8") as read_file:
            return json.load(read_file)
    except FileNotFoundError:
        return None
