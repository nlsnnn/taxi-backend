from typing import Optional
from fastapi import status


class AppException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Optional[str] = None,
    ):
        self.status_code = status_code
        self.detail = detail
