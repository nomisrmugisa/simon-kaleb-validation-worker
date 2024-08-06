"""persist data to file"""

from src.utils.constants import BASE_PATH
from src.utils.fs.json_file_handlers import save_to_json


def persist_data(data):
    """persist data to file"""
    save_to_json(data=data, file_path=f"{BASE_PATH}data.json")
