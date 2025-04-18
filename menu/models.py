from sqlmodel import SQLModel, Field
from typing import Annotated
from decimal import Decimal

class RestaurantBase(SQLModel):
    name: Annotated[str, Field()]
    latitude: Annotated[Decimal, Field(max_digits=9, decimal_places=6)]
    longitude: Annotated[Decimal, Field(max_digits=9, decimal_places=6)]
    owner_id: Annotated[int, Field()]

class Restaurant(RestaurantBase, table=True):
    __tablename__ = "restaurants"
    id: Annotated[int, Field(default=None, primary_key=True)]

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantPublic(RestaurantBase):
    id: Annotated[int, Field()]


class MenuItemBase(SQLModel):
    restaurant_id: Annotated[int, Field(foreign_key="restaurants.id")]
    name: Annotated[str, Field()]
    price: Annotated[Decimal, Field(ge=0)]
    is_available: Annotated[bool | None, Field(default=True)]

class MenuItem(MenuItemBase, table=True):
    __tablename__ = "menu_items"
    id: Annotated[int, Field(default=None, primary_key=True)]

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemPublic(MenuItemBase):
    id: Annotated[int, Field()] 