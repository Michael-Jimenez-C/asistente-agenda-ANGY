from pydantic import BaseModel
from enum import Enum

class NextType(Enum):
    CONTINUE = "continue"
    END = "end"
    WAIT_USER_RESPONSE = "wait user response"

class Parametro(BaseModel):
    nombre: str
    valor: str

class Tool(BaseModel):
    name: str
    parameters: list[Parametro]

class Format(BaseModel):
    Response: str
    tool: Tool | None = None
    next: NextType