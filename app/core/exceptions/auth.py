from fastapi import status
from app.core.exceptions.base import AppException


class AuthException(AppException):
    def __init__(
        self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: str | None = None
    ):
        super().__init__(status_code, detail)
