"""validate program area."""

import requests

from src.utils.constants import BASE_PATH, SERVICE_HOST, SERVICE_PORT
from src.progress import save_validation_progress
from src.utils.fs.json_file_handlers import load_from_json
from src.validations.validator import expression_validator
from src.validations.utils import (
    get_org_units,
    fetch_data_values,
    get_data_values,
    # data_values_post,
)


def start_validation(program_area: str, period: str, username: str, password: str):
    """start validation."""

    print("retrieving program areas from json file")
    data = load_from_json(file_path=f"{BASE_PATH}data.json")

    print(f"retrieving {program_area} data")
    program_data = data.get(program_area)
    if program_area is None:
        return {"error": f"Program area {program_area} not found"}

    print("retrieving org units")
    org_units_response = get_org_units(username, password)
    if org_units_response is None:
        return {"error": "Failed to get org units"}

    org_units = org_units_response.get("organisationUnits")
    if org_units is None:
        return {"error": "Failed to get org units"}

    url = program_data["url"]
    total_validations = len(org_units)
    number_of_completed_org_units = 0

    json_response = {}

    print(f"validating program area {program_area} for the period {period}")
    save_validation_progress(
        program_area, period, total_validations, number_of_completed_org_units
    )

    for org_unit in org_units:
        number_of_completed_org_units += 1
        org_unit_id = org_unit.get("id")

        if org_unit_id is None:
            print("Failed to get org unit id for", org_unit)
            save_validation_progress(
                program_area, period, total_validations, number_of_completed_org_units
            )
            continue

        print(f"validating org unit {org_unit_id}")
        org_unit_url = url.replace("{org_unit_id}", org_unit_id)
        org_unit_url = org_unit_url.replace("{period}", period)
        print("fetching data values for", org_unit_id)

        data_values = fetch_data_values(url=org_unit_url)
        if data_values is None:
            print(f"failed to fetch data values for {org_unit_id}")
            json_response[org_unit_id] = {
                "error": "Failed to fetch data",
                "records": [],
                "payload": None,
            }

        rows = program_data["rows"]
        records = []
        missing_data_values = {}
        passing_data_values = {}

        for value in rows:
            record = expression_validator(
                value, data_values, missing_data_values, passing_data_values
            )
            records.append(record)

        data_values = get_data_values(
            passing_data_values, missing_data_values, period, org_unit_id
        )

        error_posting_data_values = None

        # if len(data_values) > 0:
        #     print("posting data values")
            # payload = {"dataValues": data_values}
            # response = data_values_post(payload)

            # error_posting_data_values = (
            #     None if response else "Failed to post data values"
            # )

        json_response[org_unit_id] = {
            "records": records,
            "data_values": data_values,
            "error": None,
            "error_posting_data_values": error_posting_data_values,
        }

        save_validation_progress(
            program_area, period, total_validations, number_of_completed_org_units
        )

    print("done validating program area")
    print("saving validations to json")

    requests.post(
        f"http://{SERVICE_HOST}:{SERVICE_PORT}/save_validations",
        json={"data": json_response, "period": period, "program_area": program_area},
        timeout=300,
    )
