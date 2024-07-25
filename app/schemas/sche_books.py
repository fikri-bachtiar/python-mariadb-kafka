from typing import Union

from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    category: str

class BookCreate(BookBase):
    title: str
    author: str
    category: str

class Book(BookBase):
    id: int
    # owner_id: int

    class Config:
        from_attributes = True