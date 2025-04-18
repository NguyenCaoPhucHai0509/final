from fastapi import Depends
from fastapi.routing import APIRouter
from typing import Annotated

from .utils import get_current_active_user
from .models import Restaurant, RestaurantPublic

router = APIRouter()

@router.get("/test")
async def test(
    current_user: Annotated[dict, Depends(get_current_active_user)]
):
    return current_user