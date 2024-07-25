from fastapi import APIRouter, Body, status, HTTPException
from app.helpers.response import create_response
from app.helpers.enums import ResponseError

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

@router.get("/example")
async def example_endpoint():
    data = {"key": "value"}
    return create_response(error=ResponseError.NO_ERROR, message=data)

@router.get("/example-error")
async def example_error_endpoint():
    error_message = "An error occurred."
    return create_response(error=ResponseError.ERROR, message=error_message)

# #for the purpose of this illustration, a list instead of a model will be used
# fake_books_db = []

# @router.post("/create_book")
# async def create_book(new_book=Body()):
# 	for book in fake_books_db:
# 		if book['title'] == new_book['title']:
# 			return {"message": "Book with this title already exists."}
#             # raise HTTPException(status_code=400, detail="Book with this title already exists.")
	
# 	fake_books_db.append(new_book)
# 	return {"message": "Book added successfully!"}