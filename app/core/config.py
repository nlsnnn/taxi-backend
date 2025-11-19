from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    url: str


class KeycloakConfig(BaseModel):
    client_id: str
    secret: str
    base_url: str
    realm: str

    @property
    def token_url(self) -> str:
        return f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/token"

    @property
    def auth_url(self) -> str:
        return f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/auth"

    @property
    def logout_url(self) -> str:
        return f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/logout"

    @property
    def userinfo_url(self) -> str:
        return f"{self.base_url}/realms/{self.realm}/protocol/openid-connect/userinfo"


class GeneralConfig(BaseModel):
    base_url: str

    @property
    def redirect_uri(self) -> str:
        return f"{self.base_url}/api/login/callback"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP__",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    db: DatabaseConfig
    kc: KeycloakConfig
    general: GeneralConfig


settings = Settings()
