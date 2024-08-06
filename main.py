"""app entry point"""

from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.save_data.save_data_to_file import persist_data
from src.utils.validations import ValidateProgramArea
from src.validations import start_validation

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    """health check."""
    return "Server is running"


@app.post("/save_data")
async def save_data(data: Dict[Any, Any]):
    """save data"""
    persist_data(data)


@app.post("/validate")
async def validate_program_area(data: ValidateProgramArea):
    """validate program area"""

    start_validation(data.program_area, data.period, data.username, data.password)
