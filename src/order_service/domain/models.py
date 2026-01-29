from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid6


class OrderStatus(StrEnum):
    NEW = "NEW"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"


@dataclass(kw_only=True)
class Order:
    id: UUID
    user_id: str
    quantity: int
    item_id: UUID
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, *, user_id: str, quantity: int, item_id: UUID) -> Order:
        return cls(
            id=uuid6(),
            user_id=user_id,
            quantity=quantity,
            item_id=item_id,
            status=OrderStatus.NEW,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
