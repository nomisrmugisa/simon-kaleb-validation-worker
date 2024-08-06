"""validate program area"""

from pydantic import BaseModel


class ValidateProgramArea(BaseModel):
    """ValidateProgramArea class"""

    program_area: str
    period: str
    username: str
    password: str
