from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

from order_service.domain.models import OrderStatus

metadata = MetaData()

order_table = Table(
    "orders",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", String(36), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("item_id", UUID(as_uuid=True), nullable=False),
    Column("status", Enum(OrderStatus), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)

create_order_idempotency_keys = Table(
    "create_order_idempotency_keys",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "order_id",
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False,
        unique=True,
    ),
)
