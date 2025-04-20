from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, Optional, TYPE_CHECKING
from decimal import Decimal

if TYPE_CHECKING:
    from .menu_items import MenuItem

class RestaurantBase(SQLModel):
    name: Annotated[str, Field()]
    latitude: Annotated[Decimal, Field(max_digits=9, decimal_places=6)]
    longitude: Annotated[Decimal, Field(max_digits=9, decimal_places=6)]
    # could have create_at, updated_at

class Restaurant(RestaurantBase, table=True):
    __tablename__ = "restaurants"
    id: Annotated[int, Field(default=None, primary_key=True)]
    owner_id: Annotated[int, Field()]

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantPublic(RestaurantBase):
    id: Annotated[int, Field()]
    owner_id: Annotated[int, Field()]