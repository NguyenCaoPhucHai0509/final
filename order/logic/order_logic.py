from sqlmodel import Session

from ..crud.order_crud import add_order
from ..crud.order_item_crud import add_order_items
from ..models.orders import Order
from ..models.order_items import OrderItem, OrderItemCreate
from ..utils.menu_item_utils import get_menu_item_by_ids

"""We can still commit TWICE. But for responding the data of inserted order and order items,
we can only do once commit because it needs time to sync"""
async def create_order_with_order_items(
    session: Session, customer_id: int, restaurant_id: int, items: list[OrderItemCreate]
):
    # Inserting order into DB, get indetifier of this order to pass to order items
    order_db = Order(customer_id=customer_id, restaurant_id=restaurant_id)
    add_order(session, order_db)

    ids = [item.menu_item_id for item in items] # This is for getting multiple menu items by their ids
    menu_item_data = await get_menu_item_by_ids(ids) # This is for getting item's prices

    # Initializing OrderItem for adding to DB
    order_items_db = []
    for i in range(len(menu_item_data)):
        menu_item_id, quantity = items[i].menu_item_id, items[i].quantity
        price = menu_item_data[i]["price"]

        order_items_db.append(
            OrderItem(order_id=order_db.id, menu_item_id=menu_item_id, 
                      quantity=quantity, price=price)
        )
    add_order_items(session, order_items_db)

    session.commit() # ONLY 1 COMMIT HERE

    # Query DB again to get order and order items inserted to DB
    session.refresh(order_db)
    for order_item in order_items_db:
        session.refresh(order_item)

    return order_db, order_items_db