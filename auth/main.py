from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from .routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START: AUTH")
    create_db_and_tables()
    yield
    print("STOP: AUTH")

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/auth", tags=["Auth"])