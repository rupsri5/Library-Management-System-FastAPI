from fastapi import APIRouter, HTTPException, Response
from app.models.user import Student
from app.database.mongodb import collection

app = APIRouter()

@app.post("/student", response_model=Student, status_code=201)
def create_student(user: Student):
    try:
        # Check if the student already exists
        existing_student = collection.find_one({"name": user.name})
        # print(existing_student)
        if existing_student:
            raise HTTPException(status_code=400, detail="Student already exists")

        # Insert the user data into the database
        inserted_user = collection.insert_one(user.model_dump(by_alias=True))
   
        created_user = collection.find_one({"_id": inserted_user.inserted_id})
        
        return {
            "id": str(created_user["_id"]),
            "name": created_user["name"],
            "age": user.age,  
            "address": user.address  
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))