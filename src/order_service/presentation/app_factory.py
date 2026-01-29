from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from order_service.presentation.exception_handlers import register_exception_handlers
from order_service.presentation.router import router
from order_service.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI, settings: Settings) -> AsyncGenerator[None]:
    engine = create_async_engine(settings.postgres_connection_string)
    app.state.database_engine = engine
    app.state.settings = settings

    try:
        yield
    finally:
        await engine.dispose()


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(lifespan=lambda app: lifespan(app, settings))
    app.include_router(router)
    register_exception_handlers(app)
    return app
