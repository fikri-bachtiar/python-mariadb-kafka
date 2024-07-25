import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.routers import books

from app.crud import books as books_crud
from app.models import books as books_model
from app.schemas import books as books_schemas
from app.db.base import SessionLocal, engine

books_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_project_name,
              description='Base frame with FastAPI micro framework + MariaDB + Kafka',
              version=settings.app_project_version)

app.include_router(books.router)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"error": 1, "message": "api endpoint does not exist"},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": 1, "message":{"detail": exc.detail}},
    )

if __name__ == '__main__':
    uvicorn.run(app, host=settings.app_running_host, port=settings.app_running_port)