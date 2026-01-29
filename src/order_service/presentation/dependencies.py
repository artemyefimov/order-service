from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncEngine

from order_service.application.create_order import CreateOrder
from order_service.application.get_order_by_id import GetOrderByID
from order_service.infrastructure.catalog_service_client import CatalogServiceClient
from order_service.infrastructure.unit_of_work import UnitOfWork, unit_of_work
from order_service.settings import Settings


async def provide_settings(request: Request) -> Settings:
    return request.app.state.settings


async def provide_database_engine(request: Request) -> AsyncEngine:
    return request.app.state.database_engine


async def provide_unit_of_work(
    engine: Annotated[AsyncEngine, Depends(provide_database_engine)],
) -> UnitOfWork:
    return unit_of_work(engine)


async def provide_catalog_service_client(
    settings: Annotated[Settings, Depends(provide_settings)],
) -> CatalogServiceClient:
    return CatalogServiceClient(
        base_url=settings.capashino_base_url,
        api_key=settings.capashino_api_key,
    )


async def provide_create_order(
    unit_of_work: Annotated[UnitOfWork, Depends(provide_unit_of_work)],
    catalog_service_client: Annotated[
        CatalogServiceClient, Depends(provide_catalog_service_client)
    ],
) -> CreateOrder:
    return CreateOrder(unit_of_work, catalog_service_client)


async def provide_get_order_by_id(
    unit_of_work: Annotated[UnitOfWork, Depends(provide_unit_of_work)],
) -> GetOrderByID:
    return GetOrderByID(unit_of_work)
