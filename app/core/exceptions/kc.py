from fastapi import status
from app.core.exceptions.base import AppException


class KeycloakException(AppException):
    def __init__(
        self, status_code: int = status.HTTP_400_BAD_REQUEST, detail: str | None = None
    ):
        super().__init__(status_code, detail)
