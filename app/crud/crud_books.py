# from fastapi import Depends
from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from app.models import model_books
from app.schemas import sche_books


def get_all_book(db: Session):
    return db.query(model_books.Book).all()


def get_book_by_category(db: Session, category: str):
    return db.query(model_books.Book).filter(model_books.Book.category == category).all()


def get_book_by_title(db: Session, title: str):
    return db.query(model_books.Book).filter(model_books.Book.title == title).first()


def create_new_book(db: Session, book: sche_books.BookCreate):
    db_book = model_books.Book(title=book.title, author=book.author, category=book.category)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_existing_book(db: Session, title: str, book: sche_books.BookCreate):
    db_book = db.query(model_books.Book).filter(model_books.Book.title == title).first()
    if db_book:
        db_book.title = Column(book.title, String)
        db_book.author = Column(book.author, String)
        db_book.category = Column(book.category, String)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_existing_book(db: Session, title: str):
    db_book = db.query(model_books.Book).filter(model_books.Book.title == title).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
