from sqlalchemy import Column, Integer, String

from app.db.base import Base

# from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), index=True)
    author = Column(String(100), index=True)
    category = Column(String(100), index=True)
