from fastapi import HTTPException
from sqlmodel import Session, select

from ..models.menu_items import MenuItem

def get_menu_items_by_restaurant_id(
    session: Session, restaurant_id: int,
    offset: int = 0, limit: int = 100
):
    menu_items_db = session.exec(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
    ).all()

    return menu_items_db