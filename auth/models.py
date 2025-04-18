from sqlmodel import SQLModel, Field
from pydantic import EmailStr, BaseModel
from typing import Annotated
from enum import Enum

class TokenData(BaseModel):
    username: Annotated[str | None, Field(default=None)]

class UserRole(str, Enum):
    customer = "customer"
    restaurant_owner = "restaurant_owner"
    kitchen_staff = "kitchen_staff"
    delivery_driver = "delivery_driver"
    support_staff = "support_staff"

class UserBase(SQLModel):
    email: Annotated[EmailStr, Field()]
    username: Annotated[str, Field(unique=True)]
    user_role: Annotated[UserRole, Field(default=UserRole.customer)]

class User(UserBase, table=True):
    __tablename__ = "users"

    id: Annotated[int, Field(default=None, primary_key=True)]
    hashed_password: Annotated[str, Field()]
    is_active: Annotated[bool, Field(default=True)]

class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=3)]

class UserPublic(UserBase):
    id: Annotated[int, Field()]
    is_active: Annotated[bool, Field()]