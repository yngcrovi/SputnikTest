from pydantic_settings import BaseSettings, SettingsConfigDict

class PostgresURL(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    model_config = SettingsConfigDict(env_file="../.env.dev", extra='ignore', env_file_encoding='utf-8')

    def get_url(self, user: str = None, password: str = None) -> str:
        return f"postgresql+asyncpg://{user or self.POSTGRES_USER}:{password or self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"