from fastapi import Depends, Body, Query, Path
from fastapi.routing import APIRouter
from typing import Annotated
from sqlmodel import Session

from ..utils.auth_utils import (
    require_role
)
from ..crud.restaurant_crud import (
    get_restaurants
)
from ..logic.restaurant_logic import (
    create_restaurant_for_onwer
)
from ..models.restaurants import (
    RestaurantCreate, RestaurantPublic,
)
from ..models.menu_items import (
    MenuItemCreate, MenuItemPublic
)
from ..database import get_session

router = APIRouter()
"""
Create a restaurant, 
Actors: restaurant owner
"""
@router.post("/restaurants", response_model=RestaurantPublic)
async def create_restaurant_(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Depends(require_role(["restaurant_owner"]))],
    restaurant: Annotated[RestaurantCreate, Body()]
):
    return create_restaurant_for_onwer(session, current_user["id"], restaurant)


"""
List all restaurants
Actors: all
"""
@router.get("/restaurants", response_model=list[RestaurantPublic])
async def read_restaurants(
    *,
    session: Annotated[Session, Depends(get_session)],
    offset: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100
):
    return get_restaurants(session, offset, limit)