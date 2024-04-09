from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from typing import Optional, Annotated
from enum import Enum

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserType(str, Enum):
    ops = "ops"
    student = "student"

class User(BaseModel):
    # id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_type: UserType = Field(..., description="Type of User")
    name: str = Field(..., description="User's name")
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., description="Hashed password", private=True)

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str = Field(..., description="User's name")
    username: str = Field(..., description="Set Student's unique username")
    age: int = Field(..., gt=0, description="User's age")
    address: Address = Field(..., description="User's address including city and country")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rupali",
                "username": "rupali",
                "age": 21,
                "address": {
                    "city": "Delhi",
                    "country": "India"
                }
            }
        }

class StudentIDResponse(BaseModel):
    student_id: str

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, description="User's name")
    age: Optional[int] = Field(None, gt=0, description="User's age")
    address: Optional[Address] = Field(None, description="User's address including city and country")
