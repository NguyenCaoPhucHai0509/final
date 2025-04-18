from fastapi import HTTPException, Request, status, Header, Depends
import httpx
from typing import Annotated

AUTH_SERVICE_URL = "http://localhost:8000/auth"

def get_auth_header(authorization: Annotated[str, Header()]):

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    
    return authorization

async def get_current_active_user(auth_header: Annotated[str, Depends(get_auth_header)]):

    async with httpx.AsyncClient() as client:
        try:
            response: httpx.Response = await client.get(
                    url=f"{AUTH_SERVICE_URL}/me", 
                    headers={"Authorization": auth_header}
            )
            response.raise_for_status()
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
        except httpx.HTTPStatusError as exc:
            print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
    return response.json()

def require_role(user: dict, allowed_roles: list[str]):
    if user.get("role") not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )