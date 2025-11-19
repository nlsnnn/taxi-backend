from typing import Annotated
from fastapi import Depends, Request
from app.core.models.user import User
from app.services.keycloak import KeycloakClient
from app.core.exceptions import AuthException, KeycloakException


def get_keycloak_client(request: Request) -> KeycloakClient:
    """Get KeycloakClient from app.state"""
    return request.app.state.keycloak_client


async def get_token_from_cookie(request: Request) -> str | None:
    return request.cookies.get("access_token")


async def get_current_user(
    token: str = Depends(get_token_from_cookie),
    keycloak: KeycloakClient = Depends(get_keycloak_client),
) -> dict:
    if not token:
        raise AuthException(detail="No access token")

    try:
        user_info = await keycloak.get_user_info(token)
        return user_info
    except KeycloakException:
        raise AuthException(detail="Invalid token")


DependsCurrentUser = Annotated[User, Depends(get_current_user)]