from fastapi import Depends, Path, Body, HTTPException
from fastapi.routing import APIRouter
from sqlmodel import Session

from ..models.orders import OrderStatus
from ..models.order_items import (
    OrderItemPublicV2, OrderItemUpdate, OrderItem, OrderItemStatus
)
import redis.asyncio as redis
import json
from decimal import Decimal
from ..database import get_session
from ..use_cases import order_item_uc
from ..utils import auth_utils, status_utils


router = APIRouter(prefix="/order-items")

redis_client = redis.Redis()

"""
View an order item
Actor: kitchen staff
"""
@router.get("/{id}")
async def read_order_item(): pass

"""
The kitchen staff accepts this order item. Assign this 
order item to a kitchen staff. Currently, don't check wheather
kitchen staff belongs to the restarant in order
Actors: kitchen staff
"""
@router.patch("/{id}/accept", response_model=OrderItemPublicV2)
async def accept_order_item(
    session: Session = Depends(get_session),
    current_kitchen_staff: dict = Depends(auth_utils.get_current_kitchen_staff_info),
    id: int = Path()
):
    
    # Query order item in database
    order_item_db = session.get(OrderItem, id)
    if not order_item_db:
        raise HTTPException(status_code=404, detail="Order item not found")

    # Check that kitchen staff belongs to this branch
    if (current_kitchen_staff["branch_id"] != order_item_db.order.branch_id):
        raise HTTPException(
            status_code=400,
            detail="You don't belong to this restaurant"
        )
    
    # Update order status to preparing if its current status is pending
    current_order = order_item_db.order
    if current_order.status == OrderStatus.pending:
        current_order.status = OrderStatus.preparing
        session.add(current_order)
        session.commit()
 
    order_item_db.sqlmodel_update({
        "kitchen_staff_id": current_kitchen_staff["user_id"],
        "status": OrderItemStatus.preparing
    })
    session.commit()
    session.refresh(order_item_db)
    return order_item_db

"""
Change status of an order item from preparing to ready
Actors: kitchen staff
"""
@router.patch("/{id}/status")
async def change_order_item_status(
    session: Session = Depends(get_session),
    current_kitchen_staff: dict = Depends(auth_utils.get_current_kitchen_staff_info),
    id: int = Path(),
    order_item: OrderItemUpdate = Body()
):
    # Query order item in database
    order_item_db = session.get(OrderItem, id)
    if not order_item_db:
        raise HTTPException(status_code=404, detail="Order item not found")

    # Check that kitchen staff belongs to restaurant in ORDER
    if (current_kitchen_staff["branch_id"] != order_item_db.order.branch_id):
        raise HTTPException(
            status_code=400,
            detail="You don't belong to this restaurant"
        )
    
    order_item_data = order_item.model_dump(exclude_unset=True)

    # Check status change, it will raise error if invalid
    status_utils.validate_status_change(
        order_item_db.status, 
        order_item_data["status"], 
        level="order_item"
    )
    
    order_item_db.sqlmodel_update(order_item_data)
    session.commit()

    if order_item_uc.are_all_order_items_of_order_ready(order_item_db.order):
        current_order = order_item_db.order
        total_amount = Decimal(sum(order_item.price * order_item.quantity 
                        for order_item in current_order.order_items))
        
        print(f"TOTAL AMOUNTT: {total_amount}")
        current_order.sqlmodel_update({
            "status": OrderStatus.ready_for_delivery,
            "total_amount": total_amount
        })
        
        session.add(current_order)
        session.commit()
        
        delivery_payload = {
            "order_id": current_order.id
        }
        await redis_client.publish("ready_order_channel", json.dumps(delivery_payload))
    
    session.refresh(order_item_db)
    return order_item_db

#  openapi_extra={
#         "requestBody": {
#             "content": {
#                 "application/json": {
#                     "example": {
#                         "status": "ready"
#                     }
#                 }
#             }
#         }
#     }