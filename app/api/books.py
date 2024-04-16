# from fastapi import APIRouter, HTTPException, Depends
# from typing import List, Optional
# from app.models.book import Book, BookResponse
# from app.database.mongodb import collection_b
# from bson import ObjectId
# from app.api.auth import get_current_user

# book_routes = APIRouter()

# @book_routes.post("/books", response_model=BookResponse, status_code=201, response_model_by_alias=False)
# def add_book(book: Book, current_user: dict = Depends(get_current_user())):
#     try:
#         if (current_user.get("user_type") == "student"):
#             raise HTTPException(status_code=403, detail="As a student you are not allowed to perform this task")

#         book_exist = collection_b.find_one({"name": book.name, "book_category": book.book_category})
#         if book_exist:
#             raise HTTPException(status_code=400, detail="Book already exists.")

#         inserted_book = collection_b.insert_one(book.model_dump(by_alias=True))
#         book_id = str(inserted_book.inserted_id)
#         created_book = collection_b.find_one({"_id": inserted_book.inserted_id})
#         return {
#             "book_id": book_id,
#             "book_category": created_book["book_category"],
#             "name": created_book["name"]
#         }
    
#     except HTTPException as e:
#         raise e
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @book_routes.get("/books", response_model=List[Book])
# def get_all_books(category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
#     try:
#         filters = {}
#         if category:
#             filters["book_category"] = category
#         if min_price is not None:
#             filters["price"] = {"$gte": min_price}
#         if max_price is not None:
#             filters["price"] = {"$lte": max_price}

#         books = collection_b.find(filters)
#         if not books:
#             raise HTTPException(status_code=404, detail="No Books found in library")
        
#         return books
    
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @book_routes.delete("/books/{book_id}")
# def delete_book(book_id: str, current_user: dict = Depends(get_current_user())):
#     try:
#         if (current_user.get("user_type") == "student"):
#             raise HTTPException(status_code=403, detail="As a student you are not allowed to perform this task")

#         book_exist = collection_b.find_one({"_id": ObjectId(book_id)})
#         if not book_exist:
#             raise HTTPException(status_code=404, detail="Book not found")

#         collection_b.delete_one({"_id": ObjectId(book_id)})
        
#         return {"message": "Book deleted successfully"}
        
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))