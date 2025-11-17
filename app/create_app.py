from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import register_routers
from app.core.db.helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


def create_fastapi_app():
    app = FastAPI(lifespan=lifespan)

    register_routers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost",
            "http://frontend",
            "http://frontend:80",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
