from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

# Import your router from users.py
from app.api.users import user_routes
from app.api.books import book_routes

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mount static files for Swagger UI

# Redirect root URL to Swagger UI

# Include routes from users_router
app.include_router(user_routes)
app.include_router(book_routes)

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Generate custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API for Library Management System",
        version="1.0.0",
        description="This is an API for Library management system Developed with FastAPI, Python and MongoDB",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://yourlogo.com/logo.png",
        "altText": "Your Logo",
    }
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Add security requirement for JWT token to each path
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
