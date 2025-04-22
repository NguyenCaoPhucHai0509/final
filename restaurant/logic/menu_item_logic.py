from sqlmodel import Session

from ..models.menu_items import MenuItem, MenuItemCreate
from .restaurant_logic import check_ownership
from ..crud.menu_item_crud import create_menu_item

def create_menu_item_with_ownership(
    session: Session, current_owner_id: int, restaurant_id: int, 
    menu_item: MenuItemCreate
):
    # Check that this user is actually the owner of this restaurant
    check_ownership(session, current_owner_id, restaurant_id)

    menu_item_db = MenuItem.model_validate(menu_item, 
                    update={"restaurant_id": restaurant_id})
    
    return create_menu_item(session, menu_item_db)