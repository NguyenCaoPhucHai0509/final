from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from .routes import orders, order_items

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START: FOOD ORDER")
    create_db_and_tables()
    yield
    print("STOP: FOOD ORDER")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router, tags=["Order"])
app.include_router(order_items.router, tags=["Order Item"])