from pydantic import BaseModel, model_validator

from enum import Enum
from datetime import datetime

class Solicitud(BaseModel):
    solicitud: str
    proc: str | None = None