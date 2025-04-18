from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from .routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START: MENU")
    create_db_and_tables()
    yield
    print("STOP: MENU")

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/menu", tags=["Menu"])