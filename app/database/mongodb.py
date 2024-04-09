from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
 
client = MongoClient(os.getenv("MONGODB_URI"), int(os.getenv("PORT")))
db = client["libStudents"]
collection_st = db["students"]
collection_u = db["users"]
collection_b = db["books"]