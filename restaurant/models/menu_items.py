from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, Optional
from decimal import Decimal

from ..models.restaurants import Restaurant

class MenuItemBase(SQLModel):
    name: Annotated[str, Field()]
    price: Annotated[Decimal, Field(ge=0)]
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