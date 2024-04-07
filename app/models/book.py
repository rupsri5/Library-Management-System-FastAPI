from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class BookCategory(str, Enum):
    fiction = "Fiction"
    non_fiction = "Non-Fiction"
    sci_fi = "Sci-Fi"
    mystery = "Mystery"
    fantasy = "Fantasy"

class Book(BaseModel):
    book_category: BookCategory = Field(..., description="Category of the book")
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