from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime
from typing import Annotated, TYPE_CHECKING
from .order_items import OrderItemCreate

class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class OrderBase(SQLModel):
    customer_id: Annotated[int, Field()]
    restaurant_id: Annotated[int, Field()]

class Order(OrderBase, table=True):
    __tablename__ = "orders"
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    status: Annotated[OrderStatus, Field(default=OrderStatus.pending)]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]

class OrderCreate(SQLModel):
    restaurant_id: Annotated[int, Field()]
    items: Annotated[list["OrderItemCreate"], Field()]

class OrderPublic(OrderBase):
    id: Annotated[int, Field()]
    status: Annotated[OrderStatus, Field()]
    created_at: Annotated[datetime, Field()]
