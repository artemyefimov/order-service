from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine

from order_service.infrastructure.order_repository import OrderRepository

type UnitOfWork = AbstractAsyncContextManager[Repositories]


@asynccontextmanager
async def unit_of_work(engine: AsyncEngine) -> AsyncGenerator[Repositories]:
    async with engine.begin() as connection:
        yield Repositories(orders=OrderRepository(connection))


class Repositories:
    _orders: OrderRepository

    def __init__(self, orders: OrderRepository) -> None:
        self._orders = orders

    @property
    def orders(self) -> OrderRepository:
        return self._orders
