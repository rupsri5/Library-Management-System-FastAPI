from fastapi import APIRouter, HTTPException, Query, Depends
from app.models.user import Student, StudentIDResponse, StudentUpdate, User
from app.database.mongodb import collection_st, collection_u
from bson import ObjectId
from app.api.auth import generate_jwt_token, get_current_user
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_routes = APIRouter()

@user_routes.post("/signup", status_code=201)
def signup(user: User):
    try:
        existing_user = collection_u.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists, try using another email")
        
        hashed_password = pwd_context.hash(user.password)
        user.password = hashed_password
        
        inserted_user = collection_u.insert_one(user.model_dump())

        created_user = collection_u.find_one({"_id": inserted_user.inserted_id})
        user_id = str(inserted_user.inserted_id)
        token = generate_jwt_token({"_id": user_id, "user_type": created_user["user_type"]})

        return ({"message": f"{user.user_type} user signup successful", "token": token})  

    except HTTPException as e:
        raise e     
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@user_routes.post("/login", status_code=200)
def login(user: User):
    try:
        existing_user = collection_u.find_one({"email": user.email, "user_type": user.user_type})
        if existing_user and pwd_context.verify(user.password, existing_user['password']):
            user_id = str(existing_user["_id"])
            token = generate_jwt_token({"_id": user_id, "user_type": existing_user["user_type"]})
            return ({"message": f"{user.user_type} user login successful", "token": token})  
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials, check email, password and user type combination")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_routes.post("/student", response_model=StudentIDResponse, status_code=201, response_model_by_alias=False)
def create_student(user: Student, current_user: dict = Depends(get_current_user())):
    try:
        if (current_user.get("user_type") == "ops"):
            raise HTTPException(status_code=403, detail="As a ops user you are not allowed to perform this task")

        existing_student = collection_st.find_one({"username": user.username})
    
        if existing_student:
            raise HTTPException(status_code=400, detail="Student already exists")

        # Insert the user data into the database
        inserted_user = collection_st.insert_one(user.model_dump(by_alias=True))

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
                  min_age: int = Query(None, description="Only records which have age greater than equal to the provided age should be present in the result."), current_user: dict = Depends(get_current_user())):
    try:
        if (current_user.get("user_type") == "student"):
            raise HTTPException(status_code=403, detail="As a student you are not allowed to perform this task")

        # Construct filter criteria based on provided query parameters
        filter_criteria = {}
        if country:
            filter_criteria["address.country"] = country
        if city:
            filter_criteria["address.city"] = city
        if min_age:
            filter_criteria["age"] = {"$gt": min_age}

        # Retrieve filtered students from the database
        filtered_students = collection_st.find(filter_criteria)
        
        # Convert _id fields to strings and construct response data
        response_data = []
        for student in filtered_students:
            response_data.append(student)

        return response_data
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_routes.get("/student/{student_id}", response_model=Student, response_model_by_alias=False, status_code=200)
def get_student(student_id: str, current_user: dict = Depends(get_current_user())):
    try:
        if (current_user.get("user_type") == "student"):
            raise HTTPException(status_code=403, detail="As a student you are not allowed to perform this task")

        # Retrieve the student from the database
        student = collection_st.find_one({"_id": ObjectId(student_id)})
        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_routes.patch("/student/{student_id}", status_code=204)
def update_info(student_id: str, user: StudentUpdate, current_user: dict = Depends(get_current_user())):
    try:
        if (current_user.get("user_type") == "ops"):
            raise HTTPException(status_code=403, detail="As a ops user you are not allowed to perform this task")

        student_exist = collection_st.find_one({"_id": ObjectId(student_id)})
        if not student_exist:
            raise HTTPException(status_code=404, detail="Student not found")

        student_data = user.model_dump(exclude_unset=True)
        if not student_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        collection_st.update_one({"_id": ObjectId(student_id)}, {"$set": student_data})
        
        return {"message": "Student data updated successfully"}
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_routes.delete("/student/{student_id}", status_code=200)
def delete_student(student_id: str, current_user: dict = Depends(get_current_user())):
    try:
        if (current_user.get("user_type") == "ops"):
            raise HTTPException(status_code=403, detail="As a ops user you are not allowed to perform this task")

        student_exist = collection_st.find_one({"_id": ObjectId(student_id)})
        if not student_exist:
            raise HTTPException(status_code=404, detail="Student not found")
        
        collection_st.delete_one({"_id": ObjectId(student_id)})
        
        return {"message": "Student deleted successfully"}
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))