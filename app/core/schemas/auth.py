from pydantic import BaseModel

from app.core.schemas.user import SUserID


class SAddUser(SUserID):
    email: str
    email_verified: bool
    first_name: str
    last_name: str


class STokenData(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str
    expires_in: int = 3600
    refresh_expires_in: int = 2592000


class SUserInfoKC(BaseModel):
    tokens: STokenData
    info: dict
