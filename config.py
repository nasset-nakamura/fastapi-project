from pydantic import BaseSettings


class Config(BaseSettings):
    api_title: str
    api_version: str
    api_url: str
    api_port: int
    auth_admin_password: str
    auth_normal_password: str

    class Config:
        env_file = ".env"


config = Config()
