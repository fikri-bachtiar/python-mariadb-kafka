import uvicorn
from fastapi import Depends, FastAPI
from .config import settings

app = FastAPI(title=settings.app_project_name,
              description='Base frame with FastAPI micro framework + MariaDB + Kafka',
              version=settings.app_project_version)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.app_running_host, port=settings.app_running_port)