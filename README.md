
# Library Management System

This application is developed using FastAPI and Python, with MongoDB as the database. LMS is designed to efficiently manage library users and books through a secure API.

# Features
- **User Management:** LMS provides user signup and login options where users need to specify their user_type. After signup/login, a JWT token is generated for secure access to API endpoints.
- **User Roles:**
    - **Student:** Only student users can register students in the library, update their own details using PATCH requests, and delete students.
    - **Ops (Operational):** Ops users can list all registered students, search for students by student_id, add books to the library, and delete books from the library.
- **Book Management:** Both student and ops users can list all the books available in the library.


# Swagger UI Integration
The Library Management System (LMS) application integrates Swagger UI for a user-friendly interface to interact with the API endpoints. Swagger UI provides a dynamic and interactive documentation interface that allows users to explore and test the API without leaving their browser.

With Swagger UI, users can:

- View detailed documentation of available API endpoints.
- Interact with endpoints directly from the browser.
- Test API requests with ease, including authentication using JWT tokens.
- Easily understand request parameters, response formats, and error messages.
This integration enhances the usability of LMS, providing developers and users with a seamless experience for exploring and utilizing the API functionality.

You can learn more about Swagger UI [here](https://swagger.io/tools/swagger-ui/), and experience its benefits firsthand within the LMS application.


# API Endpoints
- **POST** /signup: User registration with user_type (student/ops) and generate JWT token.
- **POST** /login: User login to obtain JWT token.
- **POST** /student: Register a new student (only available for student users).
- **GET** /student: List all registered students (only available for ops users).
- **GET** /student/{student_id}: Get student details by student_id (only available for ops users).
- **PATCH** /student/{student_id}: Update current user details (only available for student users).
- **DELETE** /students/{student_id}: Delete student by student_id (only available for student users).
- **GET** /books: List all books available in the library.
- **POST** /books: Add a new book to the library (only available for ops users).
- **DELETE** /books/{book_id}: Delete book by book_id (only available for ops users).

# Major Dependencies

- **FastAPI:** FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Pydantic:** Pydantic is a data validation and settings management using Python type annotations.
- **MongoDB:** MongoDB is a general-purpose, document-based, distributed database built for modern application developers and for the cloud era.

# Installation

1. Clone the repository: 
```powershell
git clone git@github.com:rupsri5/Library-Management-System-FastAPI.git
```

2. Create virtual environment:
```powershell
python -m venv venv
```
Activate environment
For powershell:
```powershell
venv/scripts/activate
```
For Bash:
```powershell
venv/bin/activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Set up MongoDB and configure connection
You can use MongoDB Atlas for free: [MongoDB Atlas](https://www.mongodb.com/atlas/database) 
```powershell
client = MongoClient("YOUR MONGODB_URI", "PORT")
db = client["database_name_used"]
collection_st = db["collection_used"]
```

5. Run the FastAPI application:
```powershell
uvicorn main:app --reload
```

# Acknowledgment
This application is deployed on [Render](https://render.com/), a powerful platform for deploying and scaling web applications and services. Special thanks to Render for providing reliable hosting services.
