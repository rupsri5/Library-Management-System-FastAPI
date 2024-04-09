from fastapi import APIRouter, HTTPException, Query
from app.models.user import Student, StudentIDResponse, StudentUpdate
from app.database.mongodb import collection
from bson import ObjectId

user_routes = APIRouter()

@user_routes.post("/student", response_model=StudentIDResponse, status_code=201, response_model_by_alias=False)
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

        student_id = str(inserted_user.inserted_id)
        
        return {
            "student_id": student_id
        }
    
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@user_routes.get("/student", response_model=list[Student], status_code=200)
def students_list(country: str = Query(None, description="To apply filter of country."),
                  city: str = Query(None, description="To filter by city"), 
                  min_age: int = Query(None, description="Only records which have age greater than equal to the provided age should be present in the result.")):
    try:
        # Construct filter criteria based on provided query parameters
        filter_criteria = {}
        if country:
            filter_criteria["address.country"] = country
        if city:
            filter_criteria["address.city"] = city
        if min_age:
            filter_criteria["age"] = {"$gt": min_age}

        # Retrieve filtered students from the database
        filtered_students = collection.find(filter_criteria)
        
        # Convert _id fields to strings and construct response data
        response_data = []
        for student in filtered_students:
            student['_id'] = str(student['_id'])  # Convert _id to string
            response_data.append(student)

        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_routes.get("/student/{student_id}", response_model=Student, response_model_by_alias=False, status_code=200)
def get_student(student_id: str):
    try:
        # Retrieve the student from the database
        student = collection.find_one({"_id": ObjectId(student_id)})
        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_routes.patch("/student/{student_id}", status_code=204)
def update_info(student_id: str, user: StudentUpdate):
    try: 
        student_exist = collection.find_one({"_id": ObjectId(student_id)})
        if not student_exist:
            raise HTTPException(status_code=404, detail="Student not found")

        student_data = user.model_dump(exclude_unset=True)
        if not student_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        collection.update_one({"_id": ObjectId(student_id)}, {"$set": student_data})
        
        return {"message": "Student data updated successfully"}
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_routes.delete("/student/{student_id}", status_code=200)
def delete_student(student_id: str):
    try:
        student_exist = collection.find_one({"_id": ObjectId(student_id)})
        if not student_exist:
            raise HTTPException(status_code=404, detail="Student not found")
        
        collection.delete_one({"_id": ObjectId(student_id)})
        
        return {"message": "Student deleted successfully"}
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))