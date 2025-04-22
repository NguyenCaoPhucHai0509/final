from sqlmodel import SQLModel, Field
from typing import Annotated
from decimal import Decimal


class MenuItemBase(SQLModel):
    name: Annotated[str, Field()]
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2, ge=0)]
    description: Annotated[str | None, Field()] = None
    is_available: Annotated[bool | None, Field(default=True)]
    # could have create_at, updated_at

class MenuItem(MenuItemBase, table=True):
    __tablename__ = "menu_items"
    id: Annotated[int, Field(default=None, primary_key=True)]
    restaurant_id: Annotated[int, Field(foreign_key="restaurants.id")]

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemPublic(MenuItemBase):
    id: Annotated[int, Field()]
    restaurant_id: Annotated[int, Field()]

class MenuItemUpdate(SQLModel):
    restaurant_id: int | None = None
    name: str | None = None
    price: Annotated[Decimal | None, Field(ge=0)] = None
    description: str | None = None
    is_available: bool | None = None