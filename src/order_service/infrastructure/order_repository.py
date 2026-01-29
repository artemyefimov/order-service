from uuid import UUID

from sqlalchemy import RowMapping, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from order_service.domain.models import Order, OrderStatus
from order_service.exceptions import OrderNotFoundError
from order_service.infrastructure.database_schema import (
    create_order_idempotency_keys,
    order_table,
)


def order_from_row_mapping(row: RowMapping) -> Order:
    return Order(
        id=row["id"],
        user_id=row["user_id"],
        quantity=row["quantity"],
        item_id=row["item_id"],
        status=OrderStatus(row["status"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


class OrderRepository:
    _connection: AsyncConnection

    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def get_order_by_id(self, order_id: UUID) -> Order:
        cursor = await self._connection.execute(
            select(order_table).where(order_table.c.id == order_id)
        )
        row = cursor.mappings().one_or_none()

        if row is None:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")

        return order_from_row_mapping(row)

    async def get_order_created_with_idempotency_key(
        self, idempotency_key: UUID
    ) -> Order | None:
        cursor = await self._connection.execute(
            select(create_order_idempotency_keys).where(
                create_order_idempotency_keys.c.idempotency_key == idempotency_key
            )
        )
        row = cursor.mappings().one_or_none()

        if row is None:
            return None

        return await self.get_order_by_id(row["order_id"])

    async def create(self, order: Order, idempotency_key: UUID) -> None:
        await self._connection.execute(
            insert(order_table).values(
                id=order.id,
                user_id=order.user_id,
                quantity=order.quantity,
                item_id=order.item_id,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
            )
        )

        await self._connection.execute(
            insert(create_order_idempotency_keys).values(
                idempotency_key=idempotency_key,
                order_id=order.id,
            )
        )

    async def update(self, order: Order) -> None:
        await self._connection.execute(
            update(order_table)
            .where(order_table.c.id == order.id)
            .values(
                user_id=order.user_id,
                quantity=order.quantity,
                item_id=order.item_id,
                status=order.status,
                updated_at=order.updated_at,
            )
        )
