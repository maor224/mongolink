from pydantic import BaseSettings


class ConnectionSettings(BaseSettings):
    username: str
    password: str
    host: str
    port: int

    class Config:
        env_file = "src/config/.env"
