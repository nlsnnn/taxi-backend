import httpx


from app.core.config import settings
from app.core.exceptions import KeycloakException


class KeycloakClient:
    def __init__(self, client: httpx.AsyncClient = httpx.AsyncClient()):
        self.client = client

    async def get_tokens(self, code: str) -> dict:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.general.redirect_uri,
            "client_id": settings.kc.client_id,
            "client_secret": settings.kc.secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = await self.client.post(
                settings.kc.token_url, data=data, headers=headers
            )
            if response.status_code != 200:
                raise KeycloakException(401, f"Token request failed: {response.text}")
            return response.json()
        except httpx.RequestError as e:
            raise KeycloakException(500, f"Token exchange failed: {str(e)}")

    async def get_user_info(self, token: str) -> dict:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = await self.client.get(settings.kc.userinfo_url, headers=headers)
            if response.status_code != 200:
                raise KeycloakException(401, f"Invalid access token: {response.text}")
            return response.json()
        except httpx.RequestError as e:
            raise KeycloakException(500, f"Keycloak request error: {str(e)}")
