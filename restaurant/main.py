from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from .routes import restaurants, menu_items

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START: RESTAURANT")
    create_db_and_tables()
    yield
    print("STOP: RESTAURANT")

app = FastAPI(lifespan=lifespan)
app.include_router(restaurants.router, tags=["Restaurant"])
app.include_router(menu_items.router, tags=["Menu Item"])