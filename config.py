from pydantic import BaseSettings


class Config(BaseSettings):
    fastapi_url: str
    fastapi_port: int

    class Config:
        env_file = ".env"


config = Config()
