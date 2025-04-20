from fastapi import Path, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.routing import APIRouter
from sqlmodel import Session
from typing import Annotated
from datetime import timedelta


from .utils import (
    get_password_hash, authenticate, create_access_token,
    get_current_active_user
)
from .config import get_settings
from .database import get_session
from .models import User, UserCreate, UserPublic

settings = get_settings()
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()



@router.post("/register", response_model=UserPublic)
async def create_user(
    *, 
    session: Annotated[Session, Depends(get_session)],
    user: Annotated[UserCreate, Body()]
):
    hashed_password = get_password_hash(user.password)
    extra_data = {"hashed_password": hashed_password}
    user_db = User.model_validate(user, update=extra_data)
    try:
        session.add(user_db)
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User already existed"
        )
    session.commit()
    session.refresh(user_db)
    return user_db

@router.post("/login")
async def login(
    *,
    session: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate(
        session=session, 
        username=form_data.username, 
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.username)
        },
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

"""
Client must send "Authorization: Bearer <Token>" header.
When testing API, we click "Authorize" button and fill the credentials.
Then the "/auth/me" endpoints will automatic extract the Authorization header
"""
@router.get("/me", response_model=UserPublic)
async def read_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
