from sqlmodel import Session, select

from ..models.order_items import OrderItem

# Create a order item
def create_order_item(session: Session, order_item_db: OrderItem):
    session.add(order_item_db)
    session.commit()
    session.refresh(order_item_db)
    return order_item_db

"""Add multiple order items, NO COMMIT & REFRESH!. 
For composite operation (create order with order items)"""
def add_order_items(session: Session, order_items: list[OrderItem]): 
    session.add_all(order_items)