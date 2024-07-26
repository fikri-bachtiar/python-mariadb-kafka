from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import model_books
from app.schemas import sche_books


async def get_all_book(db: AsyncSession):
    result = await db.execute(select(model_books.Book))
    return result.scalars().all()


async def get_book_by_category(db: AsyncSession, category: str):
    result = await db.execute(select(model_books.Book).where(model_books.Book.category == category))
    return result.scalars().all()


async def get_book_by_title(db: AsyncSession, title: str):
    result = await db.execute(select(model_books.Book).where(model_books.Book.title == title))
    return result.scalars().all()


async def create_new_book(db: AsyncSession, book: sche_books.BookCreate):
    new_book = model_books.Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    return new_book


async def update_existing_book(db: AsyncSession, title: str, book: sche_books.BookCreate):
    result = await db.execute(
        update(model_books.Book)
        .where(model_books.Book.title == title)
        .values(**book.model_dump())
        # .returning(model_books.Book)
    )
    await db.commit()
    return result.rowcount


async def delete_existing_book(db: AsyncSession, title: str):
    result = await db.execute(
        delete(model_books.Book).where(model_books.Book.title == title)
        # .returning(model_books.Book)
    )
    await db.commit()
    return result.rowcount
