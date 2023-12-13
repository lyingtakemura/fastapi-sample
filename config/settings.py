from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: str

    JWT_SECRET_KEY: str = None
    ALGORITHM: str = None

    def get_postgres_url(self):
        return "postgresql://{}:{}@{}:5432/{}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_NAME,
        )


settings = Settings()
postgres_url = settings.get_postgres_url()
