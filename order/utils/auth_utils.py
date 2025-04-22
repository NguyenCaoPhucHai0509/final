from fastapi import HTTPException, status, Header, Depends
from typing import Annotated
from httpx import AsyncClient

from .http_call_utils import http_call

AUTH_SERVICE_URL = "http://localhost:8001/auth"

def get_auth_header(authorization: Annotated[str, Header()]):

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    
    return authorization

async def get_current_active_user(auth_header: Annotated[str, Depends(get_auth_header)]):
    async def call(client: AsyncClient):
        return await client.get(
                        url=f"{AUTH_SERVICE_URL}/me", 
                        headers={"Authorization": auth_header}
                    )
    return await http_call(call)
   
def require_role(allowed_roles: list[str]):
    def checker(current_user: dict = Depends(get_current_active_user)):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return current_user
    return checker