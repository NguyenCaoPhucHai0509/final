from fastapi import Depends, Body
from fastapi.routing import APIRouter
from sqlmodel import Session
from typing import Annotated

from ..models.orders import OrderCreate
from ..database import get_session
from ..utils.auth_utils import require_role
from ..logic.order_logic import create_order_with_order_items

router = APIRouter()

@router.get("/health")
async def health():
    return {"message": "ok"}

"""
Create an order that includes list of order items
"""
@router.post("/orders")
async def create_order(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[dict, Depends(require_role(["customer"]))],
    order: Annotated[OrderCreate, Body()]
): 
    
    order_db, order_items_db = await create_order_with_order_items(
                session, current_user["id"], order.restaurant_id, order.items)
    return {
        "message": "Create Order successfully", 
        "order": order_db, 
        "order_items": order_items_db
    }