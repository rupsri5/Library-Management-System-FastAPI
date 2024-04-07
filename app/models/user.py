from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str = Field(..., description="User's name")
    age: int = Field(..., gt=0, description="User's age")
    address: Address = Field(..., description="User's address including city and country")

    class Config:
        schema_extra = {
            "example": {
                "name": "Rupali",
                "age": 21,
                "address": {
                    "city": "Delhi",
                    "country": "India"
                }
            }
        }