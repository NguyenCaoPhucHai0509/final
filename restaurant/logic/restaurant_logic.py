from fastapi import HTTPException
from sqlmodel import Session

from ..models.restaurants import Restaurant
from ..models.menu_items import MenuItem

def check_ownership(
    session: Session, current_owner_id: int, restaurant_id: int,
):
    restaurant_db = session.get(Restaurant, restaurant_id)
    if restaurant_db.owner_id != current_owner_id:
        raise HTTPException(
            status_code=400,
            detail="You do not own this restaurant"
        )
    
def create_menu_item_with_ownership(
    session: Session, current_owner_id: int, restaurant_id: int, 
    menu_item: dict
):
    # Check that this user is actually the owner of this restaurant
    check_ownership(session, current_owner_id, restaurant_id)

    menu_item_db = MenuItem.model_validate(menu_item, 
                        update={"restaurant_id": restaurant_id})
    
    session.add(menu_item_db)
    session.commit()
    session.refresh(menu_item_db)
    return menu_item_db
    