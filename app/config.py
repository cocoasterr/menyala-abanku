from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_CONFIG:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRES_IN: int
    REFRESH_TOKEN_EXPIRES_IN: int
    JWT_PRIVATE_KEY:str
    JWT_PUBLIC_KEY:str
    class Config:
        env_file = './.env'


settings = Settings()
