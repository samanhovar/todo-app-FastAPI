from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as task_router
from users.routes import router as user_router


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
