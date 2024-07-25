from sqlalchemy.orm import Session

from app.models import books
from app.schemas import books

def get_all_book(db: Session):
    return db.query(books.Book).all()

def get_book_by_category(db: Session, category: str):
    return db.query(books.Book).filter(books.Book.category == category).first()

def create_new_book(db: Session, book: books.BookCreate):
    db_book = books.Book(title=book.title, author=book.author, category=book.category)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book