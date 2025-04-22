from fastapi import HTTPException
from sqlmodel import Session, select, SQLModel, col

from ..models.menu_items import MenuItem

# Create a menu item
def create_menu_item(session: Session, menu_item_db: MenuItem):
    session.add(menu_item_db)
    session.commit()
    session.refresh(menu_item_db)
    return menu_item_db

# Get multiple menu items by restaurant id
def get_menu_items_by_restaurant_id(
    session: Session, restaurant_id: int,
    offset: int = 0, limit: int = 100
):
    menu_items_db = session.exec(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
        .offset(offset).limit(limit)
    ).all()

    return menu_items_db

# Get a menu item (by item id)
def get_menu_item(session: Session, item_id: int):
    item_db = session.get(MenuItem, item_id)
    if not item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_db

# Get multiple menu items by their ids
def get_menu_item_by_ids(session: Session, ids: list[int]) -> list[MenuItem]:
    menu_items = session.exec(
        select(MenuItem).where(col(MenuItem.id).in_(ids))
    ).all()
    return menu_items

# Update a menu item (by item id)
def update_menu_item(session: Session, item_id: int, item: SQLModel):
    item_db = get_menu_item(session, item_id)

    item_data = item.model_dump(exclude_unset=True)
    item_db.sqlmodel_update(item_data)

    session.add(item_db)
    session.commit()
    session.refresh(item_db)

    return item_db

# Delete a menu item (by item id)
def delete_menu_item(session: Session, item_id: int):
    item_db = get_menu_item(session, item_id)
    session.delete(item_db)
    session.commit()
    return {"message": "Item deleted"}