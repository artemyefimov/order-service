from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from order_service.application.create_order import CreateOrder
from order_service.application.get_order_by_id import GetOrderByID
from order_service.presentation.dependencies import (
    provide_create_order,
    provide_get_order_by_id,
)
from order_service.presentation.schema import (
    CreateOrderRequest,
    CreateOrderResponse,
    GetOrderByIDResponse,
)

router = APIRouter()


@router.post("/api/orders", status_code=201)
async def create_order_route(
    request: CreateOrderRequest,
    create_order: Annotated[CreateOrder, Depends(provide_create_order)],
) -> CreateOrderResponse:
    order = await create_order(
        user_id=request.user_id,
        quantity=request.quantity,
        item_id=request.item_id,
        idempotency_key=request.idempotency_key,
    )

    return CreateOrderResponse(
        id=order.id,
        user_id=order.user_id,
        quantity=order.quantity,
        item_id=order.item_id,
        status=order.status,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


@router.get("/api/orders/{order_id}", status_code=200)
async def get_order_route(
    order_id: UUID,
    get_order: Annotated[GetOrderByID, Depends(provide_get_order_by_id)],
) -> GetOrderByIDResponse:
    order = await get_order(order_id)

    return GetOrderByIDResponse(
        id=order.id,
        user_id=order.user_id,
        quantity=order.quantity,
        item_id=order.item_id,
        status=order.status,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )
