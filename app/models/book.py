from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Book(BaseModel):
    book_category: str = Field(..., description="Category of the book")
    name: str = Field(..., description="Name of the book")
    edition: Optional[str] = Field(None, description="Edition of the book")
    price: float = Field(..., description="Price of the book")

    class Config:
        schema_extra = {
            "example": {
                "book_category": "Fiction",
                "name": "Pearl in Paris",
                "edition": "1975",
                "price": 19.99,
            }
        }

class BookResponse(BaseModel):
    book_id: str
    book_category:str
    name: str