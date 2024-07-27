import os

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"), extra="allow")

    try:
        app_project_name: str = "fastapi-mariadb-kafka"
        app_project_version: str = "v1.0.0"
        app_running_host: str = "127.0.0.1"
        app_running_port: int = 8000
        app_maria_db_host: str = "127.0.0.1"
        app_maria_db_port: int = 3306
        app_maria_db_name: str = "example_database"
        app_maria_db_username: str = "example_user"
        app_maria_db_password: str = "example_password"
        app_kafka_broker: str = "127.0.0.1:29092"
    except ValidationError as exc:
        raise Warning(str(exc))


settings = Settings()
