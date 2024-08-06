"""validations utils."""

import requests

from src.utils.constants import ORG_UNITS_URL


def get_org_units(username: str, password: str):
    """get org units"""
    url = ORG_UNITS_URL

    response = requests.get(url, auth=(username, password), timeout=300)
    if response.status_code != 200:
        return None

    return response.json()


def get_credentials():
    """get credentials."""
    lines = []
    with open("./data/credentials.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    return {"username": lines[0].strip(), "password": lines[1].strip()}


def clean_hmis_data(data: dict) -> dict:
    """get hmis data."""
    rows = data.get("rows")
    dict_rows = {}

    for row in rows:
        if row[0].endswith(".HllvX50cXC0"):
            row_id = row[0].replace(".HllvX50cXC0", "")
            dict_rows[row_id] = {"row_id": row_id, "value": row[3]}
        else:
            dict_rows[row[0]] = {"row_id": row[0], "value": row[3]}

    return dict_rows


def fetch_data_values(url: str):
    """fetch data values"""
    credentials = get_credentials()
    username = credentials.get("username")
    password = credentials.get("password")
    if username is None or password is None:
        return None

    response = requests.get(url, auth=(username, password), timeout=300)
    if response.status_code != 200:
        return None

    return clean_hmis_data(response.json())


def create_data_value(data_element: str, value: int, period: str, org_unit_id: str):
    """create data value."""
    data_id = data_element if "." not in data_element else data_element.split(".")[0]

    category_option_combo = (
        data_element.split(".")[1] if "." in data_element else "HllvX50cXC0"
    )

    return {
        "dataElement": data_id,
        "categoryOptionCombo": category_option_combo,
        "attributeOptionCombo": "Lf2Axb9E6B4",
        "value": str(value),
        "period": period,
        "orgUnit": org_unit_id,
    }


def get_data_values(
    passing_data_values: dict, missing_data_values: dict, period: str, org_unit_id: str
):
    """get data values"""
    for key, value in missing_data_values.items():
        if passing_data_values.get(key):
            passing_data_values.pop(key)

    data_values = []

    for key, value in passing_data_values.items():
        data_values.append(create_data_value(key, value, period, org_unit_id))

    return data_values


def post_data_values(link, credentials, data):
    """post data values."""
    username = credentials["username"]
    password = credentials["password"]

    response = requests.post(link, auth=(username, password), json=data, timeout=300)
    if response.status_code != 200:
        return False
    return True


def data_values_post(data):
    """post data values."""
    link = "https://ug.sk-engine.cloud/sss/api/dataValueSets"
    credentials = {"username": "admin", "password": "district"}

    return post_data_values(link, credentials, data)
