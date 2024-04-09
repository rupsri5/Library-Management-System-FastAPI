from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

# Import your router from users.py
from app.api.users import user_routes

app = FastAPI()

# Mount static files for Swagger UI

# Redirect root URL to Swagger UI

# Include routes from users_router
app.include_router(user_routes)

# Generate custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="This is a sample FastAPI application with Swagger UI",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://yourlogo.com/logo.png",
        "altText": "Your Logo",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
