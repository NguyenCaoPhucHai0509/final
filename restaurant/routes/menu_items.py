from fastapi import HTTPException, Depends, Path, Body, Query
from fastapi.routing import APIRouter
from sqlmodel import Session
from typing import Annotated

from ..utils.auth_utils import require_role
from ..crud.menu_item_crud import (
    get_menu_items_by_restaurant_id, update_menu_item, 
    delete_menu_item
)
from ..models.menu_items import MenuItemPublic, MenuItemUpdate
from ..database import get_session

router = APIRouter()


"""
View the menu of a specific restaurant
Actors: all
"""
@router.get("/restaurants/{restaurant_id}/menu-items", 
            response_model=list[MenuItemPublic])
async def read_menu_items_of_restaurant(
    session: Annotated[Session, Depends(get_session)],
    restaurant_id: Annotated[int, Path()],
    offset: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100
):
    return get_menu_items_by_restaurant_id(session, restaurant_id, 
                                           offset, limit)

"""
Update a Menu Item
Actors: restaurant owner
"""
@router.put("/menu-items/{item_id}", response_model=MenuItemPublic, 
    dependencies=[Depends(require_role(["restaurant_owner"]))])
async def update_menu_item_(
    session: Annotated[Session, Depends(get_session)],
    item_id: Annotated[int, Path()],
    item: Annotated[MenuItemUpdate, Body()]
):
    return update_menu_item(session, item_id, item)


"""
Delete a Menu Item
Actors: restaurant owner
"""
@router.delete("/menu-items/{item_id}", 
    dependencies=[Depends(require_role(["restaurant_owner"]))], 
    response_description="message: Item deleted"
)
async def delete_menu_item_(
    session: Annotated[Session, Depends(get_session)],
    item_id: Annotated[int, Path()]
):
    return delete_menu_item(session, item_id)