from fastapi import HTTPException
from fastapi.routing import APIRouter
from sqlmodel import Session

from ..models.menu_items import MenuItemCreate, MenuItemPublic

router = APIRouter()

# Create a Menu Item
@router.post("/menu-items", response_model=MenuItemPublic)
async def create_menu_item(
    
):
    pass