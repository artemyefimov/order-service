from uuid import UUID

from order_service.domain.models import Order
from order_service.infrastructure.unit_of_work import UnitOfWork


class GetOrderByID:
    _unit_of_work: UnitOfWork

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def __call__(self, order_id: UUID) -> Order:
        async with self._unit_of_work as uow:
            return await uow.orders.get_order_by_id(order_id)
