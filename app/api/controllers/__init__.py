from fastapi import FastAPI

from .authentication import router as authentication_router
from .weather import router as weather_router


def setup(app: FastAPI) -> None:
    app.include_router(
        router=authentication_router,
        tags=["Authentication"]
    )
    app.include_router(
        router=weather_router,
        tags=["Weather"]
    )
