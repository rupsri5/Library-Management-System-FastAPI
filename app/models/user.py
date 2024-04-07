from pydantic import BaseModel, Field
from typing import Optional

# PyObjectId = Annotated[str, BeforeValidator(str)]

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    # student_id: Optional[PyObjectId] =Field(alias="_id")
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

class StudentIDResponse(BaseModel):
    student_id: str
    name: str
    age: int
    address: Address

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, description="User's name")
    age: Optional[int] = Field(None, gt=0, description="User's age")
    address: Optional[Address] = Field(None, description="User's address including city and country")
