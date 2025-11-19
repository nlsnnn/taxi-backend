from urllib.parse import urlencode
from loguru import logger
from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.auth import SUserInfoKC, SAddUser
from app.core.schemas.user import SUserID
from app.core.exceptions import AuthException
from app.services.keycloak import KeycloakClient
from app.core.config import settings
from app.crud import UserCRUD


class AuthService:
    @classmethod
    async def login(
        cls,
        session: AsyncSession,
        code: str | None,
        keycloak: KeycloakClient,
        response: Response,
    ):
        user_info: SUserInfoKC = await cls._get_user_info(keycloak, code)
        user_id = user_info.info.get("sub")

        user = await UserCRUD.find_one_or_none_by_id(session, user_id)
        if not user:
            user_info["id"] = user_info.pop("sub")
            await UserCRUD.add(session, SAddUser.model_validate(user_info))

        token_data = user_info.tokens
        response.set_cookie(
            key="access_token",
            value=token_data.access_token,
            httponly=True,
            secure=True,
            max_age=token_data.expires_in,
        )
        response.set_cookie(
            key="refresh_token",
            value=token_data.refresh_token,
            httponly=True,
            secure=True,
            max_age=token_data.refresh_expires_in,
        )
        response.set_cookie(
            key="id_token",
            value=token_data.id_token,
            httponly=True,
            secure=True,
            max_age=token_data.expires_in,
        )
        logger.info(f"User {user_id} logged in successfully")
        return response

    @classmethod
    async def logout(cls, request: Request):
        id_token = request.cookies.get("id_token")
        params = {
            "client_id": settings.kc.client_id,
            "post_logout_redirect_uri": settings.general.base_url,
        }
        if id_token:
            params["id_token_hint"] = id_token

        # keycloak_logout_url = f"{settings.kc.logout_url}?{urlencode(params)}"
        response = Response
        response.delete_cookie(
            key="access_token",
            httponly=True,
            secure=True,
        )
        response.delete_cookie(
            key="id_token",
            httponly=True,
            secure=True,
        )
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=True,
        )
        return response

    @classmethod
    async def _get_user_info(kc: KeycloakClient, code: str) -> SUserInfoKC:
        token_data = await kc.get_tokens(code)
        print(f'{token_data=}')
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        id_token = token_data.get("id_token")

        if not access_token:
            raise AuthException(detail="Токен доступа не найден")
        if not refresh_token:
            raise AuthException(detail="Refresh token не найден")
        if not id_token:
            raise AuthException(detail="ID token не найден")

        user_info = await kc.get_user_info(access_token)
        print(f'{user_info=}')
        if not user_info.get("sub"):
            raise AuthException(detail="ID пользователя не найден")

        return SUserInfoKC(
            access_token=access_token,
            refresh_token=refresh_token,
            id_token=id_token,
            info=user_info,
        )
