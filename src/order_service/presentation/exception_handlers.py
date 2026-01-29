from fastapi import FastAPI, Request, Response

from order_service.exceptions import (
    NotEnoughStockError,
    OrderAlreadyCreatedError,
    OrderNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        OrderAlreadyCreatedError,
        handle_order_already_created_error,
    )

    app.add_exception_handler(
        NotEnoughStockError,
        handle_not_enough_stock_error,
    )

    app.add_exception_handler(
        OrderNotFoundError,
        handle_order_not_found_error,
    )


def handle_order_already_created_error(
    request: Request, exception: Exception
) -> Response:
    return Response(status_code=409, content="Order already created")


def handle_not_enough_stock_error(request: Request, exception: Exception) -> Response:
    return Response(status_code=400, content="Not enough stock")


def handle_order_not_found_error(request: Request, exception: Exception) -> Response:
    return Response(status_code=404, content="Order not found")
