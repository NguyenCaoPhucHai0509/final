from fastapi import HTTPException
import redis.asyncio as redis
import json
from sqlmodel import Session, select
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError
from decimal import Decimal
from httpx import AsyncClient

from ..utils import restaurant_utils, http_call_utils
from ..config import get_settings
from ..models.delivery_requests import DeliveryRequest
from ..database import engine

# Call external API, OpenRouteService (ORS), to get the distance
ORS_URL = "https://api.openrouteservice.org/v2"
RATE_PER_KM = 3000
BASE_FEE = 20000
settings = get_settings()

redis_client = redis.Redis()

async def subscribe_to_new_orders():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("new_order_channel")
    print("NEW ORDER CHANNEL IS LISTENING")

    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            try:
                with Session(engine) as session:
                    # Create DeliveryRequest, add it to DB
                    delivery_request = DeliveryRequest(
                        branch_id=data["branch_id"],
                        order_id=data["order_id"],
                        customer_id=data["customer_id"],
                        dropoff_lat=data["dropoff_lat"],
                        dropoff_lon=data["dropoff_lon"]
                    )
                    session.add(delivery_request)
                    session.commit()
            except OperationalError:
                raise HTTPException(status_code=500, detail="Add DB failed")
            except ValidationError as e:
                raise HTTPException(status_code=400, detail=e.errors())
            
async def subscribe_to_ready_orders():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("ready_order_channel")

    print("READY ORDER CHANNEL IS LISTENING")

    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            try:
                with Session(engine) as session:
                    delivery_request_db = session.exec(
                        select(DeliveryRequest)
                        .where(DeliveryRequest.order_id == data["order_id"])
                    ).one()

                    delivery_request_db.is_active = True
                    session.add(delivery_request_db)
                    session.commit()
            except OperationalError:
                raise HTTPException(status_code=500, detail="Add DB failed")
            except ValidationError as e:
                raise HTTPException(status_code=400, detail=e.errors())
            
async def calculate_distance(branch_id: int, dropoff_lon: Decimal, dropoff_lat: Decimal):
    branch_db = await restaurant_utils.get_branch_by_id(branch_id)

    # print(f"BRANCH: {branch_db}")
    pickup_lon, pickup_lat = branch_db["longitude"], branch_db["latitude"]

    async def call(client: AsyncClient):
        return await client.get(
                f"{ORS_URL}/directions/driving-car",
                params={
                    "api_key": settings.ORS_API_KEY, 
                    "start": f"{pickup_lon},{pickup_lat}",
                    "end": f"{dropoff_lon},{dropoff_lat}",
                }
            )
    
    geo_data = await http_call_utils.http_call(call)
    distance_m = geo_data["features"][0]["properties"]["summary"]["distance"]
    distance_km = distance_m / 1000
    return distance_km

def calculate_shipping_fee(distance_km: Decimal):
    return BASE_FEE + (distance_km * RATE_PER_KM)

def check_customer_and_driver(current_user: dict, delivery_request_db: DeliveryRequest):
    if current_user["role"] == "customer" and current_user["id"] == delivery_request_db.customer_id:
        delivery_request_db.is_customer_confirmed = True
    elif current_user["role"] == "driver" and current_user["id"] == delivery_request_db.driver_id:
        delivery_request_db.is_driver_confirmed = True
    else: raise HTTPException(status_code=400, detail="You don't relate to this delivery request")
