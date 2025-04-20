from fastapi import HTTPException
from sqlmodel import Session, select

from ..models.restaurants import Restaurant, RestaurantCreate


# Create a restaurant
def create_restaurant(
    session: Session, owner_id: int, restaurant: RestaurantCreate
):
    restaurant_db = Restaurant.model_validate(restaurant, 
                            update={"owner_id": owner_id})
    session.add(restaurant_db)
    session.commit()
    session.refresh(restaurant_db)
    return restaurant

# Get list of restuarants
def get_restaurants(
    session: Session, offset: int = 0, limit: int = 100
):
    restaurants = session.exec(
        select(Restaurant).offset(offset).limit(limit)
    ).all()
    return restaurants

# Get a restaurant by id
def get_restaurant_by_id(
    session: Session, id: int
):
    restaurant_db = session.get(Restaurant, id)
    if not restaurant_db:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant_db