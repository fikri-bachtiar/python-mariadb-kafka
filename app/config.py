import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

class Settings(BaseSettings):
    app_project_name: str = "fastapi-mariadb-kafka"
    app_project_version: str = "v1.0.0"
    app_running_host: str = "127.0.0.1"
    app_running_port: int = 8000
    app_database_url: str = "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, '.env'))

settings = Settings()