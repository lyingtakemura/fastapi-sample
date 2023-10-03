from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_host: str
    db_port: str
    db_user: str
    db_pass: str
    db_name: str

    jwt_secret_key: str = None
    algorithm: str = None

    @property
    def SQLALCHEMY_DATABASE_URL(self):
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
