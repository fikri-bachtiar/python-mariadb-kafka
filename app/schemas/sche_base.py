from pydantic import BaseModel
from typing import Any
from app.helpers.enums import ResponseError


class DataResponse(BaseModel):
    __abstract__ = True

    error: ResponseError = ResponseError.NO_ERROR
    message: Any = ""

    def response(self, error: ResponseError, message: str):
        self.error = error
        self.message = message
        return self

    def success_response(self):
        self.error = 0
        self.message = "success"
        return self

    def failed_response(self):
        self.error = 0
        self.message = "failed"
        return self
