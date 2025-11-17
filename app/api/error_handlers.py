from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions.base import AppException


def register_error_handlers(app: FastAPI):
    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": "Resource not found"},
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
