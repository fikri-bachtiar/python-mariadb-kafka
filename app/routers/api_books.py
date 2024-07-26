from fastapi import APIRouter, Response, status

from app.crud import crud_books
from app.dependencies import DBSessionDep
from app.external import kafka_prod
from app.helpers.enums import ResponseError
from app.schemas import sche_books
from app.schemas.sche_base import DataResponse

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/create_book", status_code=status.HTTP_201_CREATED, response_model=DataResponse)
async def create_new_book(response: Response, new_book: sche_books.BookCreate, db: DBSessionDep):
    try:
        exist_book = await crud_books.get_book_by_title(db, new_book.title)
        if len(exist_book) > 0:
            return DataResponse().response(error=ResponseError.ERROR, message="book with this title already exists")
        await crud_books.create_new_book(db, new_book)
        # write to kafka topic
        kafka_prod.producer.send("post-create_book", value=new_book.model_dump_json().encode())
        kafka_prod.producer.flush()

        return DataResponse().response(error=ResponseError.NO_ERROR, message="book added successfully")
    except Exception as e:
        print(e, str(e))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))


@router.get("", status_code=status.HTTP_200_OK, response_model=DataResponse)
async def read_all_books(response: Response, db: DBSessionDep):
    try:
        books_db_data = await crud_books.get_all_book(db)
        if (books_db_data is None) or (len(books_db_data) == 0):
            return DataResponse().response(error=ResponseError.ERROR, message="no book available")
        books_response = [sche_books.Book.model_validate(book) for book in books_db_data]
        return DataResponse().response(error=ResponseError.NO_ERROR, message=books_response)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))


@router.get("/", status_code=status.HTTP_200_OK, response_model=DataResponse)
async def read_all_books_with_category(response: Response, category: str, db: DBSessionDep):
    try:
        book_category = await crud_books.get_book_by_category(db, category)
        if book_category:
            books_response = [sche_books.Book.model_validate(book) for book in book_category]
            return DataResponse().response(error=ResponseError.NO_ERROR, message=books_response)
        return DataResponse().response(error=ResponseError.ERROR, message="no book with that category available")
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))


@router.put("/update_book", status_code=status.HTTP_200_OK, response_model=DataResponse)
async def update_existing_book(
    response: Response,
    update_book: sche_books.BookCreate,
    db: DBSessionDep,
):
    try:
        return_book = await crud_books.update_existing_book(db, update_book.title, update_book)
        if return_book < 1:
            return DataResponse().response(error=ResponseError.ERROR, message="no book with that title available")
        else:
            kafka_prod.producer.send("put-update_book", value=update_book.model_dump_json().encode())
            kafka_prod.producer.flush()
            return DataResponse().response(error=ResponseError.NO_ERROR, message="book updated successfully")
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))


@router.delete("/delete_book", status_code=status.HTTP_200_OK, response_model=DataResponse)
async def delete_existing_book(response: Response, book_title: str, db: DBSessionDep):
    try:
        return_book = await crud_books.delete_existing_book(db, book_title)
        if return_book < 1:
            return DataResponse().response(error=ResponseError.ERROR, message="no book with that title available")
        else:
            kafka_prod.producer.send("delete-delete_book", value=book_title.encode())
            kafka_prod.producer.flush()
            return DataResponse().response(error=ResponseError.NO_ERROR, message="book deleted successfully")
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DataResponse().response(error=ResponseError.ERROR, message=str(e))
