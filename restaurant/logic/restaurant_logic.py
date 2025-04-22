from fastapi import HTTPException
from sqlmodel import Session

from ..crud.restaurant_crud import create_restaurant
from ..models.restaurants import Restaurant, RestaurantCreate

"""
Link this restaurant to the current user (owner)
"""
def create_restaurant_for_onwer(
    session: Session, owner_id: int, payload: RestaurantCreate
):
    restaurant_db = Restaurant.model_validate(payload, 
                        update={"owner_id": owner_id})
    return create_restaurant(session, restaurant_db)

"""
Owners have permission to manage only *their own restaurants*
"""
def check_ownership(
    session: Session, current_owner_id: int, restaurant_id: int,
):
    restaurant_db = session.get(Restaurant, restaurant_id)
    if restaurant_db.owner_id != current_owner_id:
        raise HTTPException(
            status_code=400,
            detail="You do not own this restaurant"
        )
    