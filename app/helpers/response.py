from pydantic import BaseModel
from typing import Any

class StandardResponse(BaseModel):
    error: int
    message: Any

def create_response(error: int, message: Any) -> StandardResponse:
    return StandardResponse(error=error, message=message)