class OrderServiceError(Exception):
    pass


class OrderAlreadyCreatedError(OrderServiceError):
    pass


class NotEnoughStockError(OrderServiceError):
    pass


class OrderNotFoundError(OrderServiceError):
    pass
