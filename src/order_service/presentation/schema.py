from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from order_service.domain.models import OrderStatus


class CreateOrderRequest(BaseModel):
    user_id: str
    quantity: int
    item_id: UUID
    idempotency_key: UUID


class CreateOrderResponse(BaseModel):
    id: UUID
    user_id: str
    quantity: int
    item_id: UUID
    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class GetOrderByIDResponse(BaseModel):
    id: UUID
    user_id: str
    quantity: int
    item_id: UUID
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
