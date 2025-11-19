from loguru import logger
from fastapi import APIRouter, Depends, Request, Response


from app.core.exceptions import AuthException
from app.core.dependencies import DependsSession
from app.core.dependencies.auth import DependsCurrentUser, get_keycloak_client
from app.services.keycloak import KeycloakClient
from app.api.auth.service import AuthService


router = APIRouter("/auth", tags=["Auth"])


@router.get("/login/callback")
async def login_callback(
    session: DependsSession,
    response: Response,
    code: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
    keycloak: KeycloakClient = Depends(get_keycloak_client),
):
    """
    Обрабатывает callback после авторизации в Keycloak.
    Получает токен, информацию о пользователе, сохраняет пользователя в БД (если нужно)
    и устанавливает cookie с токенами. Обрабатывает ошибки от Keycloak.
    """
    if error:
        logger.error(f"Keycloak error: {error}, description: {error_description}")
        raise AuthException(detail="Authorization code is required")

    if not code:
        raise AuthException(detail="Authorization code is required")

    return await AuthService.login(session, code, keycloak, response)


@router.get("/logout")
async def logout(request: Request):
    return await AuthService.logout(request)



@router.get("/me")
async def me(user: DependsCurrentUser):
    return user