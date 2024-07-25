from fastapi import APIRouter, Body, Response, status, HTTPException
from app.helpers.enums import ResponseError
from app.schemas.sche_base import ResponseSchemaBase

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

# #for the purpose of this illustration, a list instead of a model will be used
fake_books_db = []

@router.post("/create_book", status_code=status.HTTP_201_CREATED, response_model=ResponseSchemaBase)
async def create_new_book(response: Response, new_book=Body()):
	for book in fake_books_db:
		if book['title'] == new_book['title']:
			return ResponseSchemaBase().response(error=ResponseError.ERROR, message="book with this title already exists")
	
	fake_books_db.append(new_book)
	return ResponseSchemaBase().response(error=ResponseError.NO_ERROR, message="book added successfully")

@router.get('')
async def read_all_books(response: Response):
	return ResponseSchemaBase().response(error=ResponseError.NO_ERROR, message=fake_books_db)

@router.get('/')
async def read_all_books_with_category(response: Response, category: str):
	book_category = []
	for book in fake_books_db:
		if book.get('category').casefold() == category.casefold():
			book_category.append(book)
			return ResponseSchemaBase().response(error=ResponseError.NO_ERROR, message=book_category)
	return ResponseSchemaBase().response(error=ResponseError.ERROR, message="no book with that category available")

@router.put('/update_book')
async def update_book(response: Response, update_book=Body()):
	for i in range(len(fake_books_db)):
		if fake_books_db[i].get('title').casefold() == update_book.get('title').casefold():
			fake_books_db[i] = update_book
			return ResponseSchemaBase().response(error=ResponseError.NO_ERROR, message="book updated successfully")
	return ResponseSchemaBase().response(error=ResponseError.ERROR, message="no book with that title available")

@router.delete('/delete_book')
async def delete_book(response: Response, book_title: str):
	for i in range(len(fake_books_db)):
		if fake_books_db[i].get('title').casefold() == book_title.casefold():
			fake_books_db.pop(i)
			return ResponseSchemaBase().response(error=ResponseError.NO_ERROR, message="book deleted successfully")
	return ResponseSchemaBase().response(error=ResponseError.ERROR, message="no book with that title available")