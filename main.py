from fastapi import FastAPI
from app.api import users

app = FastAPI()

# Include routes from users.py
app.include_router(users.app)