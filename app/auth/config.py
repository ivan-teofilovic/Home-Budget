from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    JWT_ALGORITHM: str
    JWT_SECRET: str
    JWT_EXPIRE: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


auth_settings = AuthConfig()
