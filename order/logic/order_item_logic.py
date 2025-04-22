from sqlmodel import Session

from ..models.order_items import OrderItemCreate, OrderItem
from ..utils.menu_item_utils import get_menu_item_by_ids
from ..crud.order_item_crud import create_order_items

async def create_order_items_for_order(
    session: Session, order_id: int, items: list[OrderItemCreate]
):
    ids = [item.menu_item_id for item in items] # This is for getting multiple menu items by their ids
   
    menu_item_data = await get_menu_item_by_ids(ids) # This is for getting item's prices

    # Initlizing OrderItem to add DB
    order_items = []
    for i in range(len(menu_item_data)):
        menu_item_id, quantity = items[i].menu_item_id, items[i].quantity
        price = menu_item_data[i]["price"]

        order_items.append(
            OrderItem(order_id=order_id, menu_item_id=menu_item_id, 
                      quantity=quantity, price=price)
        )
    return create_order_items(session, order_items)
    