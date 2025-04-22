from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from .routes import orders

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START: FOOD ORDER")
    create_db_and_tables()
    yield
    print("STOP: FOOD ORDER")

app = FastAPI(lifespan=lifespan)
app.include_router(orders.router, tags=["Orders"])