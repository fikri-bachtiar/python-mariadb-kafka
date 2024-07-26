from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.db.base import sessionmanager
from app.routers import api_books


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(
    title=settings.app_project_name,
    description="Base frame with FastAPI micro framework + MariaDB + Kafka",
    version=settings.app_project_version,
)

# app.add_middleware(DBSessionMiddleware, db_url=settings.app_db_url)
app.include_router(api_books.router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"error": 1, "message": "api endpoint does not exist"},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": 1, "message": {"detail": exc.detail}},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_running_host, port=settings.app_running_port)
