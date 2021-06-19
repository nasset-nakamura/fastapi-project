from pydantic import BaseSettings


class Config(BaseSettings):
    fastapi_url: str
    fastapi_port: int
    auth_admin_password: str
    auth_normal_password: str

    class Config:
        env_file = ".env"


config = Config()
