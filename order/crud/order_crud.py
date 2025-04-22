from sqlmodel import Session, select

from ..models.orders import Order

"""Add an order, NOT COMMIT & REFRESH. 
For composite operation (create order with order items)"""
def add_order(session: Session, order_db: Order):
    session.add(order_db)
    session.flush()