"""get progress."""

import requests

from src.utils.constants import SERVICE_HOST, SERVICE_PORT


def save_validation_progress(
    program_area: str, period: str, total: int, completed: int
):
    """save validation progress"""
    print(f"saving progress for {program_area} for the period {period}")

    data = {
        "program_area": program_area,
        "period": period,
        "total": total,
        "completed": completed,
    }
    requests.post(
        f"http://{SERVICE_HOST}:{SERVICE_PORT}/update_progress", json=data, timeout=300
    )
