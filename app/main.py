import uvicorn
from fastapi import Depends, FastAPI
from .config import settings
from .routers import books

app = FastAPI(title=settings.app_project_name,
              description='Base frame with FastAPI micro framework + MariaDB + Kafka',
              version=settings.app_project_version)

app.include_router(books.router)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.app_running_host, port=settings.app_running_port)