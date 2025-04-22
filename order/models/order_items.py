from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime
from decimal import Decimal
from typing import Annotated

class OrderItemStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"

class OrderItemBase(SQLModel):
    menu_item_id: Annotated[int, Field()]
    quantity: Annotated[int, Field(gt=0)]

    # note, promo_code ???
    
class OrderItem(OrderItemBase, table=True):
    __tablename__ = "order_items"
    id: Annotated[int | None, Field(default=None, primary_key=True)]
    order_id: Annotated[int, Field(foreign_key="orders.id")]
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2, ge=0)]
    status: Annotated[OrderItemStatus, Field(default=OrderItemStatus.pending)]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]
    updated_at: Annotated[datetime, Field(default=None)]

class OrderItemCreate(OrderItemBase):
    pass
