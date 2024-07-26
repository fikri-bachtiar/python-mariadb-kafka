from fastapi import APIRouter, Body, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session

# from fastapi_sqlalchemy import db

from app.helpers.enums import ResponseError
from app.schemas.sche_base import DataResponse

# from app.schemas.sche_books import BookCreate
from app.db.base import get_db
from app.crud import crud_books
from app.schemas import sche_books

router = APIRouter(prefix="/books", tags=["books"])

# #for the purpose of this illustration, a list instead of a model will be used
# fake_books_db = []


@router.post(
    "/create_book", status_code=status.HTTP_201_CREATED, response_model=DataResponse
)
async def create_new_book(
    response: Response, new_book: sche_books.BookCreate, db: Session = Depends(get_db)
):
    try:
        exist_book = crud_books.get_book_by_title(db, new_book.title)
        if exist_book is not None:
            return DataResponse().response(
                error=ResponseError.ERROR, message="book with this title already exists"
            )
        crud_books.create_new_book(db, new_book)
        return DataResponse().response(
            error=ResponseError.NO_ERROR, message="book added successfully"
        )
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))


@router.get("", status_code=status.HTTP_200_OK, response_model=DataResponse)
async def read_all_books(response: Response, db: Session = Depends(get_db)):
    try:
        books_db_data = crud_books.get_all_book(db)
        books_response = [
            sche_books.Book.model_validate(book) for book in books_db_data
        ]
        return DataResponse().response(
            error=ResponseError.NO_ERROR, message=books_response
        )
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=DataResponse)
async def read_all_books_with_category(
    response: Response, category: str, db: Session = Depends(get_db)
):
    try:
        book_category = crud_books.get_book_by_category(db, category)
        if book_category is not None:
            books_response = [
                sche_books.Book.model_validate(book) for book in book_category
            ]
            return DataResponse().response(
                error=ResponseError.NO_ERROR, message=books_response
            )
        return DataResponse().response(
            error=ResponseError.ERROR, message="no book with that category available"
        )
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))


@router.put("/update_book", status_code=status.HTTP_200_OK, response_model=DataResponse)
async def update_book(
    response: Response,
    update_book: sche_books.BookCreate,
    db: Session = Depends(get_db),
):
    try:
        book_title = crud_books.get_book_by_title(db, update_book.title)
        if book_title is not None:
            book_title_conv = sche_books.Book.model_validate(book_title)
            crud_books.update_existing_book(db, book_title_conv.title, update_book)
            return DataResponse().response(
                error=ResponseError.NO_ERROR, message="book updated successfully"
            )
        return DataResponse().response(
            error=ResponseError.ERROR, message="no book with that title available"
        )
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))


@router.delete(
    "/delete_book", status_code=status.HTTP_200_OK, response_model=DataResponse
)
async def delete_book(
    response: Response, book_title: str, db: Session = Depends(get_db)
):
    try:
        ret_book_title = crud_books.get_book_by_title(db, book_title)
        if ret_book_title is not None:
            ret_book_title_conv = sche_books.Book.model_validate(ret_book_title)
            crud_books.delete_existing_book(db, ret_book_title_conv.title)
            return DataResponse().response(
                error=ResponseError.NO_ERROR, message="book deleted successfully"
            )
        return DataResponse().response(
            error=ResponseError.ERROR, message="no book with that title available"
        )
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))
