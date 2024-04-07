from fastapi import FastAPI
from app.api import users

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# Include routes from users.py
app.include_router(users.app)

# app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
# app.config["OPENAPI_SWAGGER_UI_URL"] =  "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"