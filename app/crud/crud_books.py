from sqlalchemy.orm import Session

from app.models import model_books
from app.schemas import sche_books

def get_all_book(db: Session):
    return db.query(model_books.Book).all()

def get_book_by_category(db: Session, category: str):
    return db.query(model_books.Book).filter(model_books.Book.category == category).first()

def create_new_book(db: Session, book: model_books.BookCreate):
    db_book = model_books.Book(title=book.title, author=book.author, category=book.category)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book