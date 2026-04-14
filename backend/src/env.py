from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    REDIS_URL: str

    model_config = SettingsConfigDict(env_file="../.env.dev", extra='ignore')

env = Env()