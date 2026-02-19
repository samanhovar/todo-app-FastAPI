from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader, APIKeyQuery
from contextlib import asynccontextmanager
from tasks.routes import router as task_router
from users.routes import router as user_router
from users.models import UserModel
from auth.basic_auth import get_authenticated_user


tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations related to task management",
        "externalDocs": {
            "description": "More about tasks",
            "url": "https://example.com/docs/tasks",
        },
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


app = FastAPI(
    title="Todo Application",
    description=(
        "A simple and efficient Todo management API built with FastAPI. "
        "This API allows users to create, retrieve, update, and delete tasks. "
        "It is designed for task tracking and productivity improvement."
    ),
    version="0.0.1",
    contact={
        "name": "Saman Ghasemi",
        "url": "https://github.com/samanhovar",
        "email": "samanghasemidesk@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(task_router)
app.include_router(user_router)


@app.get("/public")
def public_route():
    return {"message": "This is a public route."}


@app.get("/private")
def private_route(user: Annotated[UserModel, Depends(get_authenticated_user)]):
    return {"message": "This is a private route."}


header_schema = APIKeyHeader(name="x-key")

@app.get("/apikeyheader")
def api_key_header(api_key = Depends(header_schema)):
    return {"message": "This is a test for APIKeyHeader"}


query_schema = APIKeyQuery(name="api-key")

@app.get("/apikeyquery")
def api_key_query(api_key = Depends(query_schema)):
    return {"message": "This is a test for APIKeyQuery"}
