from fastapi import Depends, Body, Path
from fastapi.routing import APIRouter
from sqlmodel import Session, select
import redis.asyncio as redis
import json


from ..models.orders import (
    Order, OrderCreate, 
    OrderUpdate, OrderPublic
)
from ..models.order_items import (
    OrderItem
)
from ..database import get_session
from ..utils import auth_utils, restaurant_utils
from ..use_cases import order_uc

router = APIRouter(prefix="/orders") # Notice this prefix


# Initialize Redis client (configure host/port if needed)
redis_client = redis.Redis()

"""
Create an order that includes list of order items
Actors: customer
"""
@router.post("/", response_model=OrderPublic)
async def create_order(
    session: Session = Depends(get_session),
    current_user: dict = Depends(auth_utils.require_role(["customer"])),
    order: OrderCreate = Body()
):  
    customer_id = current_user["id"]

    menu_item_data = await restaurant_utils.get_menu_item_by_ids(
        ids=[item.menu_item_id for item in order.items]
    )

    # Create OrderItem for adding to DB
    order_items = [
        OrderItem(
            menu_item_id=order.items[i].menu_item_id, 
            quantity=order.items[i].quantity, 
            note=order.items[i].note,
            price=menu_item_data[i]["price"]
        )
        for i in range(len(menu_item_data))
    ]

    order_db = Order(
        branch_id=order.branch_id, 
        customer_id=customer_id, 
        order_items=order_items
    )

    session.add(order_db)
    session.commit()
    session.refresh(order_db)

    delivery_payload = {
        "branch_id": order_db.branch_id,
        "order_id": order_db.id,
        "customer_id": customer_id,
        "dropoff_lon": str(order.dropoff_lon),
        "dropoff_lat": str(order.dropoff_lat)
    }
    await redis_client.publish("new_order_channel", json.dumps(delivery_payload))

    return order_db

"""
View all orders of current customer
Actors: customer
"""
@router.get("/me", response_model=list[OrderPublic])
async def read_orders(
    session: Session = Depends(get_session),
    current_user: dict = Depends(auth_utils.require_role(["customer"]))
):
    return session.exec(
        select(Order).where(Order.customer_id == current_user["id"])
    ).all()

"""
View an order. Access depends on ownership/involvement
Actors: all
e.g.: 
Customer whose user_id = 2 create this order so only this customer could see this order.
This order is created in restaurant_id = 1, so the owner of this restaurant whose 
user_id = 1 could see this one. Kitchen staffs whose user_id = 3, 4, 5 cooks foods (order items)
in this order could see this one. Delivery driver whose user_id = 6 accepts/is assigned this one
and delivery this one so could see too.
"""
@router.get("/{order_id}", response_model=OrderPublic)
async def read_order(
    session: Session = Depends(get_session),
    current_user: dict = Depends(
        auth_utils.require_role(["owner", "admin", "customer", "driver"])
    ),
    order_id: int = Path()
):  
    return await order_uc.get_order_with_check_involvement(
        session, current_user, order_id
    )

"""
View orders for that restaurant
Actors: restaurant_owner
"""
# @router.get("/branch/{id}")
# async def read_orders_of_restaurant(): pass