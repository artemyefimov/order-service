from uuid import UUID

from order_service.domain.models import Order
from order_service.exceptions import NotEnoughStockError, OrderAlreadyCreatedError
from order_service.infrastructure.catalog_service_client import CatalogServiceClient
from order_service.infrastructure.unit_of_work import UnitOfWork


class CreateOrder:
    _unit_of_work: UnitOfWork
    _catalog_service_client: CatalogServiceClient

    def __init__(
        self, unit_of_work: UnitOfWork, catalog_service_client: CatalogServiceClient
    ) -> None:
        self._unit_of_work = unit_of_work
        self._catalog_service_client = catalog_service_client

    async def __call__(
        self,
        *,
        user_id: str,
        quantity: int,
        item_id: UUID,
        idempotency_key: UUID,
    ) -> Order:
        async with self._unit_of_work as uow:
            already_created_order = (
                await uow.orders.get_order_created_with_idempotency_key(idempotency_key)
            )

            if already_created_order is not None:
                raise OrderAlreadyCreatedError(
                    "Order already created with this idempotency key"
                )

            item = await self._catalog_service_client.get_catalog_item_by_id(item_id)
            if item.available_qty < quantity:
                raise NotEnoughStockError("Not enough items in stock")

            order = Order.create(user_id=user_id, quantity=quantity, item_id=item_id)
            await uow.orders.create(order, idempotency_key)

            return order
