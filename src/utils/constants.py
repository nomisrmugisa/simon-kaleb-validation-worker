"""constants."""

import os

BASE_PATH = r"C:\Program Files (x86)\Sk Engines\Portable Python-3.10.5 x64\App\System\downloads\\"

SERVICE_HOST = os.environ.get("127.0.0.1")
SERVICE_PORT = os.environ.get("8002")
ORG_UNITS_URL = os.environ.get("https://hibrid.ug.s-3.com/dhis/api/me?fields=organisationUnits[id]")
