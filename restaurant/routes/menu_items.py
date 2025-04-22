from fastapi import HTTPException, Depends, Path, Body, Query
from fastapi.routing import APIRouter
from sqlmodel import Session
from typing import Annotated

from ..utils.auth_utils import require_role
from ..crud.menu_item_crud import (
    get_menu_items_by_restaurant_id, update_menu_item, 
    delete_menu_item, get_menu_item_by_ids
)
from ..logic.menu_item_logic import (
    create_menu_item_with_ownership
)
from ..models.menu_items import (
    MenuItemPublic, MenuItemUpdate, MenuItemCreate
)
from ..database import get_session

router = APIRouter()

"""
Add a menu item to the restaurant
Actors: all
"""
@router.post("/restaurants/{restaurant_id}/menu-items", 
            response_model=MenuItemPublic)
async def create_menu_item(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Depends(require_role(["restaurant_owner"]))],
    restaurant_id: Annotated[int, Path()],
    menu_item: Annotated[MenuItemCreate, Body()]
):
    return create_menu_item_with_ownership(
        session, current_user["id"], restaurant_id, menu_item
    )

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
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Item deleted"
                    }
                }
            }
        }
    }
)
async def delete_menu_item_(
    session: Annotated[Session, Depends(get_session)],
    item_id: Annotated[int, Path()]
):
    return delete_menu_item(session, item_id)


"""
View price of multiple menu items (for Order Service)
"""
@router.get("/menu-items", include_in_schema=False)
async def read_menu_item_by_ids(
    session: Annotated[Session, Depends(get_session)], 
    ids: Annotated[list[int], Query()]
):
    return get_menu_item_by_ids(session, ids)